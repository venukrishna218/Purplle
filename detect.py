import cv2
from ultralytics import YOLO
from datetime import datetime, timezone
import uuid
from emit import emit_events
from tracker import SessionTracker  # Importing your new tracker module

# Load the fastest YOLO model for hackathon speed
model = YOLO('yolov8n.pt') 

# Initialize our custom session tracker
tracker = SessionTracker()

STORE_ID = "STORE_BLR_002"
CAMERA_ID = "CAM_MAIN_01"

def process_video(video_path: str):
    cap = cv2.VideoCapture(video_path)
    events_batch = []
    
    print(f"Starting pipeline on {video_path}...")

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        
        # Run YOLO with built-in spatial tracking
        results = model.track(frame, persist=True, classes=0, verbose=False)
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confidences = results[0].boxes.conf.cpu().tolist()
            
            for box, track_id, conf in zip(boxes, track_ids, confidences):
                if conf < 0.4: continue 
                
                # --- USE MODULAR TRACKER ---
                visitor_id, session_seq, is_new = tracker.process_track(track_id)
                
                # If they just appeared, it's an ENTRY. Otherwise, ZONE_DWELL.
                event_type = "ENTRY" if is_new else "ZONE_DWELL"
                
                event = {
                    "event_id": str(uuid.uuid4()),
                    "store_id": STORE_ID,
                    "camera_id": CAMERA_ID,
                    "visitor_id": visitor_id,
                    "event_type": event_type, 
                    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    "zone_id": "MAIN_FLOOR",
                    "dwell_ms": 1000, 
                    "is_staff": False,
                    "confidence": round(conf, 3),
                    "metadata": {
                        "queue_depth": None,
                        "session_seq": session_seq
                    }
                }
                events_batch.append(event)

        # Emit in batches of 50
        if len(events_batch) >= 50:
            emit_events(events_batch)
            events_batch = []

        # Optional: Show video feed
        # annotated_frame = results[0].plot()
        # cv2.imshow("Tracking", annotated_frame)
        # if cv2.waitKey(1) & 0xFF == ord("q"): break

    if events_batch: emit_events(events_batch)
    cap.release()
    cv2.destroyAllWindows()
    print("Video processing complete.")

if __name__ == "__main__":
    process_video(r"C:\Users\venuk\OneDrive\Desktop\Projects\Purplle\data\CAM 1.mp4") # 0 for webcam, or use "data/clip.mp4"