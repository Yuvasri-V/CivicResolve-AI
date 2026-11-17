
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ComplaintCreate(BaseModel):
    title: str = Field(min_length=5, max_length=150)
    description: str = Field(min_length=10, max_length=5000)
    area: str = Field(min_length=2, max_length=150)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    image_path: str | None = None


class ComplaintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reference_no: str
    title: str
    description: str
    category: str
    area: str
    latitude: float | None
    longitude: float | None
    priority_score: int
    priority_level: str
    status: str
    image_path: str | None = None
    image_prediction: str | None = None
    prediction_confidence: float | None = None
    priority_reason: str | None = None
    assigned_team: str | None = None
    response_at: datetime | None = None
    resolved_at: datetime | None = None
    resolution_notes: str | None = None
    resolution_deadline: datetime | None = None
    verified_at: datetime | None = None
    created_at: datetime
    is_overdue: bool = False
    community_verification: "CommunityVerificationResponse | None" = None


class VerificationCreate(BaseModel):
    voter_key: str = Field(min_length=3, max_length=100)
    vote: str = Field(pattern="^(confirm|needs_review)$")


class VerificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    complaint_id: int
    vote: str
    created_at: datetime


class VerificationSummary(BaseModel):
    complaint_id: int
    confirmations: int
    needs_review: int
    total_verifications: int
    community_status: str


class CommunityVerificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    complaint_id: int
    status: str
    confirmation_count: int
    flag_count: int
    updated_at: datetime


class StatusHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    complaint_id: int
    from_status: str | None
    to_status: str
    note: str | None
    created_at: datetime


class ComplaintDetailResponse(ComplaintResponse):
    status_history: list[StatusHistoryResponse] = []


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    complaint_id: int | None
    level: str
    title: str
    message: str
    is_read: bool
    created_at: datetime


class ComplaintUpdate(BaseModel):
    status: str | None = Field(
        default=None,
        pattern="^(Reported|Verified|In Progress|Resolved)$",
    )
    assigned_team: str | None = Field(default=None, max_length=120)
    resolution_notes: str | None = None
    mark_responded: bool = False


class AnalyticsResponse(BaseModel):
    total_complaints: int
    by_category: dict[str, int]
    by_priority: dict[str, int]
    by_status: dict[str, int]
    pending_community: int
    overdue_count: int
    avg_resolution_hours: float | None
    critical_open: int
