from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
import asyncio
import random
import cv2
import numpy as np

router = APIRouter()

def generate_frames():
    """Simulates real-time video inference frames with bounding boxes."""
    width, height = 640, 480
    while True:
        # Create a synthetic dark frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Draw a mock "YOLOv8 Car Bounding Box" floating around
        x = int(320 + int(random.uniform(-100, 100)))
        y = int(240 + int(random.uniform(-50, 50)))
        
        # Color: BGR format (Green for car)
        cv2.rectangle(frame, (x-40, y-30), (x+40, y+30), (0, 255, 0), 2)
        cv2.putText(frame, "CAR 0.95", (x-40, y-35), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

        # Draw a mock "YOLOv8 Person Bounding Box"
        px = int(150 + int(random.uniform(-20, 20)))
        py = int(300 + int(random.uniform(-10, 10)))
        
        # Color (Orange/Red for person)
        cv2.rectangle(frame, (px-15, py-40), (px+15, py+40), (0, 165, 255), 2)
        cv2.putText(frame, "PER 0.88", (px-15, py-45), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 165, 255), 1)
        
        # Add a mock Timestamp / FPS text
        cv2.putText(frame, "Live YOLOv8 Inference Stream | ~60 FPS", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@router.get("/stream")
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            simulated_inference = {
                "detections": [
                    {"class": "car", "confidence": round(random.uniform(0.7, 0.99), 2), "bbox": [100, 100, 200, 200]},
                    {"class": "person", "confidence": round(random.uniform(0.6, 0.95), 2), "bbox": [300, 300, 350, 450]}
                ],
                "risk_assessment": {
                    "ttc": round(random.uniform(1.0, 10.0), 1),
                    "warning": "None"
                }
            }
            if simulated_inference["risk_assessment"]["ttc"] < 2.0:
                simulated_inference["risk_assessment"]["warning"] = "Vehicle too close"
                
            await websocket.send_json(simulated_inference)
            await asyncio.sleep(0.1)
            
    except WebSocketDisconnect:
        print("Client disconnected from inference stream.")

@router.get("/voice-assistant")
def get_voice_warning(ttc: float):
    if ttc < 1.0:
        return {"message": "CRITICAL: Brace for impact!"}
    elif ttc < 2.5:
        return {"message": "WARNING: Vehicle too close. Brake immediately."}
    else:
        return {"message": "Path clear."}
