from typing import Optional, List
from datetime import datetime
from beanie import Document, Indexed, Link
from pydantic import EmailStr, Field


# ── User ─────────────────────────────────────────────────────────────────────

class User(Document):
    """SaaS platform user with subscription and billing fields."""
    fullname: str
    email: Indexed(EmailStr, unique=True)          # type: ignore[valid-type]
    hashed_password: str
    is_admin: bool = False
    is_active: bool = True
    subscription_plan: str = "Free"               # Free | Pro | Enterprise
    razorpay_customer_id: Optional[str] = None

    class Settings:
        name = "users"                             # MongoDB collection name


# ── Accident ──────────────────────────────────────────────────────────────────

class Accident(Document):
    """Road accident / anomaly event logged by the detection system."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    severity: str                                  # Minor | Moderate | Severe
    anomaly_type: str                              # Vehicle too close | Collision | Speeding
    license_plate: Optional[str] = None
    # Store uploader's email as a soft reference (avoids complex populate)
    uploader_email: Optional[str] = None

    class Settings:
        name = "accidents"


# ── Report ────────────────────────────────────────────────────────────────────

class Report(Document):
    """LLM-generated incident report linked to an Accident."""
    accident_id: str                               # Accident document ID as string
    generated_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "reports"
