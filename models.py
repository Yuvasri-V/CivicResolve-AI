
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Float,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    reference_no: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    area: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    latitude: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    longitude: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    priority_score: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    priority_level: Mapped[str] = mapped_column(
        String(20), default="Medium", nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30), default="Reported", nullable=False
    )

    image_path: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    image_prediction: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    prediction_confidence: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    priority_reason: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    assigned_team: Mapped[str | None] = mapped_column(
        String(120), nullable=True
    )

    response_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    resolution_notes: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    resolution_deadline: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )


class CommunityVerificationRecord(Base):
    """Module 4: one verification summary record per complaint."""

    __tablename__ = "community_verification_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    complaint_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("complaints.id"),
        unique=True,
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(40), default="Pending", nullable=False
    )

    confirmation_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    flag_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Verification(Base):
    __tablename__ = "verifications"

    __table_args__ = (
        UniqueConstraint(
            "complaint_id",
            "voter_key",
            name="uq_complaint_voter",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    complaint_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("complaints.id"),
        nullable=False,
        index=True,
    )

    voter_key: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    vote: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )


class StatusHistory(Base):
    """Module 5: resolution / workflow timeline entries."""

    __tablename__ = "status_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    complaint_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("complaints.id"),
        nullable=False,
        index=True,
    )

    from_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    to_status: Mapped[str] = mapped_column(String(30), nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    complaint_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("complaints.id"),
        nullable=True,
        index=True,
    )

    level: Mapped[str] = mapped_column(String(20), default="info", nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
