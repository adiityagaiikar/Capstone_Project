from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, close_db
import models
from routers import auth, detection, analytics, reports, emergency, payment


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.
    - startup:  connect to MongoDB and register all Beanie models
    - shutdown: close the Motor client cleanly
    """
    await init_db(document_models=[
        models.User,
        models.Accident,
        models.Report,
    ])
    yield
    await close_db()


app = FastAPI(
    title="Road Safety AI API",
    description="Core backend orchestrator for Intelligent Transport Infrastructure.",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modular Routers
app.include_router(auth.router,      prefix="/api/auth",      tags=["Authentication"])
app.include_router(detection.router, prefix="/api/detection", tags=["Real-time Detection"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Driving Behavior Analytics"])
app.include_router(reports.router,   prefix="/api/reports",   tags=["Analysis & Reports Engine"])
app.include_router(emergency.router, prefix="/api/emergency", tags=["Emergency Alert Module"])
app.include_router(payment.router,   prefix="/api/payment",   tags=["Subscription & Billing"])


@app.get("/")
def read_root():
    return {"status": "Operational", "service": "Road Safety AI API", "db": "MongoDB"}
