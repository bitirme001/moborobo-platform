from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class NodeResponse(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    weight_kg: float = Field(serialization_alias="weightKg")
    fill_percent: float = Field(serialization_alias="fillPercent")
    is_full: bool = Field(serialization_alias="isFull")
    last_seen: datetime = Field(serialization_alias="lastSeen")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_serializer("last_seen")
    def serialize_last_seen(self, value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class TelemetryCreate(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    weight_kg: float = Field(alias="weightKg")
    fill_percent: float = Field(alias="fillPercent", ge=0, le=100)
    is_full: Optional[bool] = Field(default=None, alias="isFull")
    recorded_at: Optional[datetime] = Field(default=None, alias="recordedAt")

    model_config = ConfigDict(populate_by_name=True)


class RouteResponse(BaseModel):
    ordered_node_ids: list[str]
    path: list[tuple[float, float]]
    total_distance_m: int
