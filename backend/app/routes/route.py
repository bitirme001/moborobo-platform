from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import WasteNode
from app.schemas import RouteResponse
from app.services.routing import calculate_route

router = APIRouter(tags=["route"])


@router.get("/route", response_model=RouteResponse)
def get_route(db: Session = Depends(get_db)) -> dict:
    nodes = list(db.scalars(select(WasteNode).order_by(WasteNode.id)))
    return calculate_route(nodes)
