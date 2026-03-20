from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    fullname: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

# --- Video Schemas ---
class VideoBase(BaseModel):
    filename: str

class VideoResponse(VideoBase):
    id: int
    upload_time: datetime
    status: str
    uploader_id: int

    class Config:
        from_attributes = True

# --- Accident Schemas ---
class AccidentBase(BaseModel):
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    severity: str
    anomaly_type: str
    license_plate: Optional[str] = None
    video_id: Optional[int] = None

class AccidentCreate(AccidentBase):
    pass

class AccidentResponse(AccidentBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# --- Report Schemas ---
class ReportBase(BaseModel):
    generated_text: str

class ReportResponse(ReportBase):
    id: int
    accident_id: int
    created_at: datetime

    class Config:
        from_attributes = True
