from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
import random

router = APIRouter()

@router.post("/log", response_model=schemas.AccidentResponse)
def log_incident(incident: schemas.AccidentCreate, db: Session = Depends(get_db)):
    # Severity Estimation Module - Calculate severity based on inputs
    # If weather API is integrated, it would be factored in here.
    
    new_accident = models.Accident(
        location=incident.location,
        latitude=incident.latitude,
        longitude=incident.longitude,
        severity=incident.severity,
        anomaly_type=incident.anomaly_type,
        license_plate=incident.license_plate,
        video_id=incident.video_id
    )
    db.add(new_accident)
    db.commit()
    db.refresh(new_accident)
    return new_accident

@router.post("/{accident_id}/generate-summary", response_model=schemas.ReportResponse)
def generate_llm_summary(accident_id: int, db: Session = Depends(get_db)):
    accident = db.query(models.Accident).filter(models.Accident.id == accident_id).first()
    if not accident:
        raise HTTPException(status_code=404, detail="Accident not found")
        
    # Integration with OpenAI or Gemini LLM (Placeholder)
    prompt = f"Write a professional incident report for an anomaly of type '{accident.anomaly_type}' at location '{accident.location}' with severity '{accident.severity}'."
    simulated_summary = f"On {accident.timestamp.strftime('%Y-%m-%d')}, an automated detection system flagged a {accident.severity.lower()} incident at {accident.location}. The anomaly was classified as '{accident.anomaly_type}'. Local authorities should review the associated video footage to confirm the event."
    
    report = models.Report(
        accident_id=accident.id,
        generated_text=simulated_summary
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@router.get("/")
def get_recent_incidents(limit: int = 10, db: Session = Depends(get_db)):
    incidents = db.query(models.Accident).order_by(models.Accident.timestamp.desc()).limit(limit).all()
    return incidents
