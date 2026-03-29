from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── Auth ──────────────────────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# ── User ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Serializable user payload returned by the API. Never exposes the password."""
    id: str                               # MongoDB _id as string
    fullname: str
    email: EmailStr
    is_admin: bool
    is_active: bool
    subscription_plan: str
    razorpay_customer_id: Optional[str] = None

    model_config = {"from_attributes": True}


# ── Accident ──────────────────────────────────────────────────────────────────

class AccidentCreate(BaseModel):
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    severity: str
    anomaly_type: str
    license_plate: Optional[str] = None


class AccidentResponse(AccidentCreate):
    id: str
    timestamp: datetime

    model_config = {"from_attributes": True}


# ── Report ────────────────────────────────────────────────────────────────────

class ReportResponse(BaseModel):
    id: str
    accident_id: str
    generated_text: str
    created_at: datetime

    model_config = {"from_attributes": True}
