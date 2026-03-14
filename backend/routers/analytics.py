from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/driving-score/{user_id}")
def get_driving_score(user_id: int):
    # Driving Behavior Analytics
    # In production, this pulls telemetry from the database and runs ML scoring
    
    lane_discipline = random.randint(70, 100)
    braking_frequency = random.randint(60, 100)
    acceleration_stability = random.randint(75, 100)
    speed_compliance = random.randint(50, 100)
    
    overall_score = int((lane_discipline + braking_frequency + acceleration_stability + speed_compliance) / 4)
    
    return {
        "user_id": user_id,
        "overall_score": overall_score,
        "metrics": {
            "lane_discipline": lane_discipline,
            "braking_frequency": braking_frequency,
            "acceleration_stability": acceleration_stability,
            "speed_limit_compliance": speed_compliance
        }
    }
