from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import random

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Simulate receiving a frame
            data = await websocket.receive_text()
            
            # YOLOv8 Placeholder Logic
            # In production, pass the binary frame to ultralytics YOLOv8
            
            simulated_inference = {
                "detections": [
                    {"class": "car", "confidence": round(random.uniform(0.7, 0.99), 2), "bbox": [100, 100, 200, 200]},
                    {"class": "person", "confidence": round(random.uniform(0.6, 0.95), 2), "bbox": [300, 300, 350, 450]}
                ],
                "risk_assessment": {
                    "ttc": round(random.uniform(1.0, 10.0), 1), # Time to collision
                    "warning": "None"
                }
            }
            
            # Simulated Collision Identification
            if simulated_inference["risk_assessment"]["ttc"] < 2.0:
                simulated_inference["risk_assessment"]["warning"] = "Vehicle too close"
                
            await websocket.send_json(simulated_inference)
            await asyncio.sleep(0.1) # Simulate inference delay
            
    except WebSocketDisconnect:
        print("Client disconnected from inference stream.")

@router.get("/voice-assistant")
def get_voice_warning(ttc: float):
    # Voice Assistant Support endpoint returning strings
    if ttc < 1.0:
        return {"message": "CRITICAL: Brace for impact!"}
    elif ttc < 2.5:
        return {"message": "WARNING: Vehicle too close. Brake immediately."}
    else:
        return {"message": "Path clear."}
