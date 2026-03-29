from fastapi import APIRouter, HTTPException
from datetime import datetime
import models
import schemas

router = APIRouter()


@router.post("/log", response_model=schemas.AccidentResponse, status_code=201)
async def log_incident(incident: schemas.AccidentCreate):
    """Log a new road accident / anomaly event to MongoDB."""
    new_accident = models.Accident(
        location=incident.location,
        latitude=incident.latitude,
        longitude=incident.longitude,
        severity=incident.severity,
        anomaly_type=incident.anomaly_type,
        license_plate=incident.license_plate,
    )
    await new_accident.insert()
    return _accident_to_response(new_accident)


@router.post("/{accident_id}/generate-summary", response_model=schemas.ReportResponse)
async def generate_llm_summary(accident_id: str):
    """
    Generate a simulated LLM incident report for an accident.
    Replace the simulated_summary with a real OpenAI / Gemini call when ready.
    """
    from beanie import PydanticObjectId
    accident = await models.Accident.get(PydanticObjectId(accident_id))
    if not accident:
        raise HTTPException(status_code=404, detail="Accident not found")

    simulated_summary = (
        f"On {accident.timestamp.strftime('%Y-%m-%d')}, an automated detection system flagged a "
        f"{accident.severity.lower()} incident at {accident.location}. "
        f"The anomaly was classified as '{accident.anomaly_type}'. "
        "Local authorities should review the associated camera footage to confirm the event."
    )

    report = models.Report(
        accident_id=accident_id,
        generated_text=simulated_summary,
    )
    await report.insert()

    return schemas.ReportResponse(
        id=str(report.id),
        accident_id=accident_id,
        generated_text=report.generated_text,
        created_at=report.created_at,
    )


@router.get("/")
async def get_recent_incidents(limit: int = 10):
    """Return the most recent accident documents, newest first."""
    accidents = (
        await models.Accident.find()
        .sort(-models.Accident.timestamp)
        .limit(limit)
        .to_list()
    )
    return [_accident_to_response(a) for a in accidents]


# ── Helper ────────────────────────────────────────────────────────────────────

def _accident_to_response(a: models.Accident) -> schemas.AccidentResponse:
    return schemas.AccidentResponse(
        id=str(a.id),
        location=a.location,
        latitude=a.latitude,
        longitude=a.longitude,
        severity=a.severity,
        anomaly_type=a.anomaly_type,
        license_plate=a.license_plate,
        timestamp=a.timestamp,
    )
