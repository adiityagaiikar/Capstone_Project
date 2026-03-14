from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    
    videos = relationship("Video", back_populates="uploader")

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Uploaded") # Uploaded, Processing, Completed
    uploader_id = Column(Integer, ForeignKey("users.id"))
    
    uploader = relationship("User", back_populates="videos")
    accidents = relationship("Accident", back_populates="video")

class Accident(Base):
    __tablename__ = "accidents"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    severity = Column(String) # Minor, Moderate, Severe
    anomaly_type = Column(String) # Vehicle too close, Collision Detected, Speeding
    license_plate = Column(String, nullable=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=True)
    
    video = relationship("Video", back_populates="accidents")
    report = relationship("Report", back_populates="accident", uselist=False)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    accident_id = Column(Integer, ForeignKey("accidents.id"), unique=True)
    generated_text = Column(Text) # LLM Generated Natual Language Report
    created_at = Column(DateTime, default=datetime.utcnow)
    
    accident = relationship("Accident", back_populates="report")
