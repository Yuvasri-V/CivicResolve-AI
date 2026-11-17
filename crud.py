from .models import StatusHistory
from .models import Notification
from datetime import datetime, timedelta
from sqlalchemy import func
from uuid import uuid4
from sqlalchemy.orm import Session

from .models import (
    Complaint,
    Verification,
    CommunityVerificationRecord,
    StatusHistory,
)
from .schemas import ComplaintCreate
from .ai_classifier import predict_category
from .priority_engine import assess_priority


# Automatically assign the responsible department
def _assign_team(category: str) -> str:
    category = category.strip().lower()

    team_mapping = {
        "road": "Roads Crew",
        "roads": "Roads Crew",
        "water": "Water & Drainage",
        "drainage": "Water & Drainage",
        "electricity": "Electrical Safety",
        "electrical": "Electrical Safety",
        "safety": "Electrical Safety",
        "sanitation": "Sanitation",
    }

    return team_mapping.get(category, "General Review")


# Set a resolution deadline based on priority
def _priority_deadline(priority_level: str):
    hours_mapping = {
        "P1 - Urgent": 24,
        "P2 - High": 72,
        "P3 - Medium": 168,
        "P4 - Low": 336,
        "Urgent": 24,
        "High": 72,
        "Medium": 168,
        "Low": 336,
    }

    hours = hours_mapping.get(priority_level, 168)
    return datetime.now() + timedelta(hours=hours)


# Create a complaint with automatic predictions
def create_complaint(
    db: Session,
    data: ComplaintCreate,
) -> Complaint:

    # 1. Predict complaint category
    category = predict_category(
        data.title,
        data.description,
    )

    # 2. Calculate priority
    priority = assess_priority(
        data.title,
        data.description,
        category,
    )

    priority_level = priority["priority_level"]

    # 3. Create complaint with automatically assigned values
    complaint = Complaint(
        reference_no=f"CR-{uuid4().hex[:10].upper()}",
        title=data.title,
        description=data.description,
        area=data.area,
        latitude=data.latitude,
        longitude=data.longitude,

        category=category,
        assigned_team=_assign_team(category),

        priority_score=priority["priority_score"],
        priority_level=priority_level,
        priority_reason=priority.get(
            "priority_reason",
            "Priority assessed from complaint details",
        ),

        resolution_deadline=_priority_deadline(priority_level),

        status="Reported",
        image_path=data.image_path,
    )

    try:
        db.add(complaint)
        db.flush()

        # Create a community verification record
        ensure_community_record(db, complaint.id)

        db.commit()
        db.refresh(complaint)

        return complaint

    except Exception:
        db.rollback()
        raise


# Submit a community verification
def create_verification(
    db: Session,
    complaint_id: int,
    voter_key: str,
    vote: str,
):
    complaint = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if complaint is None:
        return None, "Complaint not found"

    existing = (
        db.query(Verification)
        .filter(
            Verification.complaint_id == complaint_id,
            Verification.voter_key == voter_key,
        )
        .first()
    )

    if existing:
        return None, "You have already verified this complaint"

    verification = Verification(
        complaint_id=complaint_id,
        voter_key=voter_key,
        vote=vote,
    )

    try:
        db.add(verification)
        db.commit()
        db.refresh(verification)

        return verification, None

    except Exception:
        db.rollback()
        raise


# Count community verification results
def get_verification_summary(
    db: Session,
    complaint_id: int,
):
    complaint = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if complaint is None:
        return None

    rows = (
        db.query(
            Verification.vote,
            func.count(Verification.id),
        )
        .filter(Verification.complaint_id == complaint_id)
        .group_by(Verification.vote)
        .all()
    )

    counts = {vote: count for vote, count in rows}
    confirmations = counts.get("confirm", 0)
    needs_review = counts.get("needs_review", 0)

    return {
        "complaint_id": complaint_id,
        "confirmations": confirmations,
        "needs_review": needs_review,
        "total_verifications": confirmations + needs_review,
    }


# Get complaints with optional filters
def get_all_complaints(
    db: Session,
    category: str | None = None,
    priority: str | None = None,
    status: str | None = None,
    area: str | None = None,
):
    query = db.query(Complaint)

    if category:
        query = query.filter(Complaint.category == category)

    if priority:
        query = query.filter(
            Complaint.priority_level == priority
        )

    if status:
        query = query.filter(Complaint.status == status)

    if area:
        query = query.filter(Complaint.area == area)

    return query.order_by(Complaint.id.desc()).all()


# Create a community verification record if one does not exist
def ensure_community_record(
    db: Session,
    complaint_id: int,
):
    record = (
        db.query(CommunityVerificationRecord)
        .filter(
            CommunityVerificationRecord.complaint_id
            == complaint_id
        )
        .first()
    )

    if record is None:
        record = CommunityVerificationRecord(
            complaint_id=complaint_id
        )
        db.add(record)
        db.flush()

    return record


def backfill_complaint_predictions(db: Session):
    """Fill missing prediction fields for existing complaints."""

    complaints = db.query(Complaint).all()
    updated_count = 0

    try:
        for complaint in complaints:
            changed = False

            # Predict category only when missing or pending
            if (
                not complaint.category
                or complaint.category == "Pending AI Analysis"
            ):
                category = predict_category(
                    complaint.title,
                    complaint.description,
                )
                complaint.category = category
                changed = True
            else:
                category = complaint.category

            # Calculate priority when score or level is missing/pending
            if (
                complaint.priority_score is None
                or complaint.priority_level is None
                or complaint.priority_level == "Pending"
            ):
                priority = assess_priority(
                    complaint.title,
                    complaint.description,
                    category,
                )

                complaint.priority_score = priority["priority_score"]
                complaint.priority_level = priority["priority_level"]

                if hasattr(complaint, "priority_reason"):
                    complaint.priority_reason = priority.get(
                        "priority_reason",
                        "Priority assessed from complaint details",
                    )

                changed = True

            # Assign a team only when missing
            if not complaint.assigned_team:
                complaint.assigned_team = _assign_team(category)
                changed = True

            # Add a deadline only when missing
            if not complaint.resolution_deadline:
                if complaint.priority_level:
                    complaint.resolution_deadline = _priority_deadline(
                        complaint.priority_level
                    )
                    changed = True

            if changed:
                updated_count += 1

        db.commit()
        return updated_count

    except Exception:
        db.rollback()
        raise

    
def list_notifications(db: Session):
    """Return the newest notifications first."""
    return (
        db.query(Notification)
        .order_by(Notification.created_at.desc())
        .all()
    )

# Get a complaint using its reference number
def get_complaint_by_reference(
    db: Session,
    reference_no: str,
):
    return (
        db.query(Complaint)
        .filter(Complaint.reference_no == reference_no)
        .first()
    )


# Get complaint details using its database ID

def get_complaint_detail(
    db: Session,
    complaint_id: int,
):
    complaint = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if complaint is None:
        return None

    status_history = (
        db.query(StatusHistory)
        .filter(StatusHistory.complaint_id == complaint_id)
        .order_by(StatusHistory.created_at.desc())
        .all()
    )

    return {
        "status_history": status_history,
    }
