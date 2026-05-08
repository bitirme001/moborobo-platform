from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import WasteNode


SEED_NODES = [
    ("N1", "Engineering Gate", 39.86782, 32.74894, 12.4, 41, False, "2026-05-06T17:42:00Z"),
    ("N2", "Library Square", 39.86834, 32.75008, 24.9, 91, True, "2026-05-06T17:44:00Z"),
    ("N3", "Cafeteria North", 39.86911, 32.75136, 16.8, 57, False, "2026-05-06T17:46:00Z"),
    ("N4", "Dorm Entrance", 39.86976, 32.75221, 14.2, 38, False, "2026-05-06T17:49:00Z"),
    ("N5", "Lab Block A", 39.87021, 32.75361, 27.3, 95, True, "2026-05-06T17:50:00Z"),
    ("N6", "Admin Garden", 39.86948, 32.75492, 10.6, 29, False, "2026-05-06T17:53:00Z"),
    ("N7", "Sports Hall", 39.86877, 32.75584, 26.1, 89, True, "2026-05-06T17:56:00Z"),
    ("N8", "Student Center", 39.86794, 32.75448, 11.3, 34, False, "2026-05-06T17:58:00Z"),
]


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def seed_nodes(db: Session) -> None:
    has_nodes = db.scalar(select(WasteNode.id).limit(1))
    if has_nodes:
        return

    db.add_all(
        WasteNode(
            id=node_id,
            name=name,
            lat=lat,
            lng=lng,
            weight_kg=weight_kg,
            fill_percent=fill_percent,
            is_full=is_full,
            last_seen=parse_utc(last_seen),
        )
        for node_id, name, lat, lng, weight_kg, fill_percent, is_full, last_seen in SEED_NODES
    )
    db.commit()
