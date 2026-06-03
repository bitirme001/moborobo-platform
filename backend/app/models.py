from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class WasteNode(Base):
    __tablename__ = "waste_nodes"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    fill_percent: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    is_full: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    telemetry_readings: Mapped[list["TelemetryReading"]] = relationship(
        back_populates="node",
        cascade="all, delete-orphan",
    )


class TelemetryReading(Base):
    __tablename__ = "telemetry_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    node_id: Mapped[str] = mapped_column(ForeignKey("waste_nodes.id"), index=True, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    fill_percent: Mapped[float] = mapped_column(Float, nullable=False)
    is_full: Mapped[bool] = mapped_column(Boolean, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)

    node: Mapped[WasteNode] = relationship(back_populates="telemetry_readings")
