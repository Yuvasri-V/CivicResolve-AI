
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .database import Base, engine, get_db, test_connection, SessionLocal
from .schema_migrate import ensure_complaint_columns
from . import crud, schemas
from .image_utils import save_uploaded_image
from .websocket_manager import manager


def _backfill_community_records() -> None:
    db = SessionLocal()
    try:
        for complaint in crud.get_all_complaints(db):
            crud.ensure_community_record(db, complaint.id)
        db.commit()
    finally:
        db.close()


# ADDED: Fill eligible missing prediction fields in existing complaints
def _backfill_predictions() -> None:
    db = SessionLocal()
    try:
        updated = crud.backfill_complaint_predictions(db)
        print(f"Updated {updated} existing complaints.")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ensure_complaint_columns(engine)
    try:
        _backfill_community_records()

        # ADDED: Run the prediction backfill during startup
        _backfill_predictions()

    except SQLAlchemyError as error:
        print(f"Database startup error: {error}")

    yield


app = FastAPI(
    title="CivicResolve AI",
    description="Public grievance reporting and tracking API",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def broadcast_events(events: list[dict]) -> None:
    for event in events:
        await manager.broadcast(event)


@app.get("/")
def home():
    return {"message": "CivicResolve AI API is running"}


@app.get("/api/health")
def health():
    try:
        test_connection()
        return {"api": "ok", "database": "connected"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed. Check MySQL settings.",
        )


@app.websocket("/ws/live")
async def websocket_live(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# MODULE 2: Complaint submission
@app.post(
    "/api/complaints",
    response_model=schemas.ComplaintResponse,
    status_code=201,
)
async def submit_complaint(
    data: schemas.ComplaintCreate,
    db: Session = Depends(get_db),
):
    try:
        complaint = crud.create_complaint(db, data)
        events = crud.build_create_events(complaint)
        await broadcast_events(events)
        detail = crud.get_complaint_detail(db, complaint.id)
        return detail
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save the complaint.",
        )


# MODULE 2 / 6: List complaints (optional filters for admin)
@app.get(
    "/api/complaints",
    response_model=list[schemas.ComplaintResponse],
)
def list_complaints(
    category: str | None = None,
    priority: str | None = None,
    status: str | None = None,
    area: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_all_complaints(
        db,
        category=category,
        priority=priority,
        status=status,
        area=area,
    )


# MODULE 4: Nearby complaints for community map/list
@app.get("/api/complaints/nearby")
def nearby_complaints(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(5.0, gt=0, le=50),
    db: Session = Depends(get_db),
):
    return crud.get_nearby_complaints(db, latitude, longitude, radius_km)


# MODULE 2: Track a complaint by reference number
@app.get(
    "/api/complaints/by-reference/{reference_no}",
    response_model=schemas.ComplaintDetailResponse,
)
def track_complaint(
    reference_no: str,
    db: Session = Depends(get_db),
):
    complaint = crud.get_complaint_by_reference(db, reference_no)

    if complaint is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found. Check the reference number.",
        )

    detail = crud.get_complaint_detail(db, complaint.id)
    return detail


@app.get(
    "/api/complaints/{complaint_id}",
    response_model=schemas.ComplaintDetailResponse,
)
def complaint_detail(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    detail = crud.get_complaint_detail(db, complaint_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return detail


# MODULE 4: Submit a community verification
@app.post("/api/complaints/{complaint_id}/verifications")
async def submit_verification(
    complaint_id: int,
    verification: schemas.VerificationCreate,
    db: Session = Depends(get_db),
):
    try:
        verification_obj, error, events = crud.create_verification(
            db=db,
            complaint_id=complaint_id,
            voter_key=verification.voter_key,
            vote=verification.vote,
        )

        if error == "Complaint not found":
            raise HTTPException(status_code=404, detail=error)

        if error:
            raise HTTPException(status_code=409, detail=error)

        await broadcast_events(events)

        return {
            "message": "Verification submitted successfully",
            "id": verification_obj.id,
            "complaint_id": verification_obj.complaint_id,
            "vote": verification_obj.vote,
            "created_at": verification_obj.created_at,
            "events": events,
        }

    except HTTPException:
        raise
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save the verification.",
        )


# MODULE 4: Get community verification totals
@app.get(
    "/api/complaints/{complaint_id}/verifications/summary",
    response_model=schemas.VerificationSummary,
)
def verification_summary(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    summary = crud.get_verification_summary(
        db=db,
        complaint_id=complaint_id,
    )

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    return summary


@app.get(
    "/api/complaints/{complaint_id}/community-verification",
    response_model=schemas.CommunityVerificationResponse,
)
def community_verification_record(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    record = crud.get_community_record(db, complaint_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    db.commit()
    return record


# MODULE 5: Timeline history
@app.get(
    "/api/complaints/{complaint_id}/history",
    response_model=list[schemas.StatusHistoryResponse],
)
def complaint_history(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    complaint = crud.get_complaint_by_id(db, complaint_id)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    return crud.get_complaint_detail(db, complaint_id)


# MODULE 5: Notifications feed
@app.get(
    "/api/notifications",
    response_model=list[schemas.NotificationResponse],
)
def notifications(db: Session = Depends(get_db)):
    return crud.list_notifications(db)


# MODULE 6: Admin analytics
@app.get("/api/admin/analytics", response_model=schemas.AnalyticsResponse)
def admin_analytics(db: Session = Depends(get_db)):
    return crud.get_analytics(db)


# MODULE 6: Admin update (assign, status, resolution)
@app.patch(
    "/api/admin/complaints/{complaint_id}",
    response_model=schemas.ComplaintResponse,
)
async def admin_update_complaint(
    complaint_id: int,
    data: schemas.ComplaintUpdate,
    db: Session = Depends(get_db),
):
    complaint, events = crud.update_complaint_admin(db, complaint_id, data)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    await broadcast_events(events)
    detail = crud.get_complaint_detail(db, complaint.id)
    return detail


@app.post("/api/images/upload")
async def upload_accident_image(
    file: UploadFile = File(...)
):
    try:
        image_bytes = await file.read()
        image_path = save_uploaded_image(image_bytes)

        return {
            "message": "Image uploaded successfully",
            "image_path": image_path
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    finally:
        await file.close()
