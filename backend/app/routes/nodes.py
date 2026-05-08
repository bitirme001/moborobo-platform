from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TelemetryReading, WasteNode, utc_now
from app.schemas import NodeResponse, TelemetryCreate

router = APIRouter(tags=["nodes"])


@router.get("/nodes", response_model=list[NodeResponse], response_model_by_alias=True)
def list_nodes(db: Session = Depends(get_db)) -> list[WasteNode]:
    return list(db.scalars(select(WasteNode).order_by(WasteNode.id)))


@router.get("/nodes/{node_id}", response_model=NodeResponse, response_model_by_alias=True)
def get_node(node_id: str, db: Session = Depends(get_db)) -> WasteNode:
    node = db.get(WasteNode, node_id)
    if node is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    return node


@router.post("/nodes/{node_id}/telemetry", response_model=NodeResponse, response_model_by_alias=True)
def record_telemetry(
    node_id: str,
    payload: TelemetryCreate,
    db: Session = Depends(get_db),
) -> WasteNode:
    node = db.get(WasteNode, node_id)
    if node is None:
        if payload.lat is None or payload.lng is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="lat and lng are required when creating a new node",
            )
        node = WasteNode(
            id=node_id,
            name=payload.name or f"Node {node_id}",
            lat=payload.lat,
            lng=payload.lng,
        )
        db.add(node)

    recorded_at = payload.recorded_at or utc_now()
    node.name = payload.name or node.name
    node.lat = payload.lat if payload.lat is not None else node.lat
    node.lng = payload.lng if payload.lng is not None else node.lng
    node.weight_kg = payload.weight_kg
    node.fill_percent = payload.fill_percent
    node.is_full = payload.is_full if payload.is_full is not None else payload.fill_percent >= 85
    node.last_seen = recorded_at.astimezone(timezone.utc)

    db.add(
        TelemetryReading(
            node=node,
            weight_kg=node.weight_kg,
            fill_percent=node.fill_percent,
            is_full=node.is_full,
            recorded_at=node.last_seen,
        )
    )
    db.commit()
    db.refresh(node)
    return node
