from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import auth, detection, analytics, reports, emergency

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Road Safety AI API",
    description="Core backend orchestrator for Intelligent Transport Infrastructure.",
    version="1.0.0"
)

# CORS Configuration for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Modular Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(detection.router, prefix="/api/detection", tags=["Real-time Detection"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Driving Behavior Analytics"])
app.include_router(reports.router, prefix="/api/reports", tags=["Analysis & Reports Engine"])
app.include_router(emergency.router, prefix="/api/emergency", tags=["Emergency Alert Module"])

@app.get("/")
def read_root():
    return {"status": "Operational", "service": "Road Safety AI API"}
