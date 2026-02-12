import cv2
import torch
import torch.nn as nn
import numpy as np
import threading
import time
import os
from ultralytics import YOLO
import supervision as sv
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights

# --- 1. WEAPON DETECTION SETUP ---
try:
    weapon_model_path = "best.pt" if os.path.exists("best.pt") else "yolov5su.pt"
    weapon_model = YOLO(weapon_model_path)
    tracker = sv.ByteTrack()
    smoother = sv.DetectionsSmoother(length=5)
    box_annotator = sv.BoxAnnotator(thickness=2)
    label_annotator = sv.LabelAnnotator(text_thickness=2, text_scale=0.7)
    print(f"✅ Weapon Model Loaded: {weapon_model_path}")
except Exception as e:
    print(f"❌ Weapon Model Error: {e}")
    weapon_model = None

# --- 2. VIOLENCE DETECTION SETUP ---
class MockViolenceModel(nn.Module):
    def forward(self, x):
        return torch.tensor([[0.1]])

try:
    from model import ViolenceModel
    print("✅ Found 'model.py', using real architecture.")
except ImportError:
    print("⚠️ 'model.py' not found. Using MockViolenceModel.")
    ViolenceModel = MockViolenceModel

violence_model = None
violence_device = "cuda" if torch.cuda.is_available() else "cpu"
violence_buffer = []
SEQUENCE_LENGTH = 16
THRESHOLD = 0.65  # Lowered slightly to be more sensitive

try:
    violence_model = ViolenceModel().to(violence_device)
    if os.path.exists("violence_model.pth"):
        try:
            violence_model.load_state_dict(torch.load("violence_model.pth", map_location=violence_device), strict=False)
            print("✅ Violence Model Weights Loaded")
        except RuntimeError as e:
            print(f"⚠️ Weights Mismatch. Switching to Mock Mode.")
            violence_model = MockViolenceModel().to(violence_device)
    else:
        print("⚠️ 'violence_model.pth' not found. Running in Mock Mode.")
    violence_model.eval()
except Exception as e:
    print(f"❌ Violence Model Critical Error: {e}")
    violence_model = MockViolenceModel().to(violence_device)

# --- 3. PROCESSING FUNCTIONS ---

def process_weapon_frame(frame):
    if not weapon_model: return frame
    
    results = weapon_model(frame, imgsz=640, conf=0.4, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    
    # Filter for weapon classes
    target_keywords = ["pistol", "knife", "gun", "weapon", "firearm", "rifle"]
    selected_class_ids = [id for id, name in weapon_model.names.items() if any(k in name.lower() for k in target_keywords)]
    
    if selected_class_ids:
        detections = detections[np.isin(detections.class_id, selected_class_ids)]

    detections = tracker.update_with_detections(detections)
    detections = smoother.update_with_detections(detections)
    
    labels = [f"{weapon_model.names[cid].upper()} {conf:.2f}" for cid, conf in zip(detections.class_id, detections.confidence)]
    
    annotated_frame = box_annotator.annotate(scene=frame.copy(), detections=detections)
    return label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)

def process_violence_frame(frame):
    global violence_buffer
    if not violence_model: return frame

    try:
        # Preprocessing matched to training (Resize -> Normalize 0-1)
        resized = cv2.resize(frame, (224, 224))
        # Ensure float32 and normalize
        normalized = resized.astype(np.float32) / 255.0
        violence_buffer.append(normalized)

        if len(violence_buffer) > SEQUENCE_LENGTH:
            violence_buffer.pop(0)

        prob = 0.0
        label = "NORMAL"
        color = (0, 255, 0) # Green

        if len(violence_buffer) == SEQUENCE_LENGTH:
            # Create batch: (1, Channels, Frames, H, W) -> (1, 3, 16, 224, 224)
            clip = np.array(violence_buffer)
            # Permute to (Channels, Frames, H, W)
            clip = torch.from_numpy(clip).permute(3, 0, 1, 2).unsqueeze(0).to(violence_device)

            with torch.no_grad():
                output = violence_model(clip)
                # Handle sigmoid vs raw logits
                prob = torch.sigmoid(output).item()
                
                # DEBUG: Print probability to console
                print(f"👊 Violence Score: {prob:.4f}")

        if prob > THRESHOLD:
            label = "VIOLENCE"
            color = (0, 0, 255) # Red

        # Draw UI
        cv2.rectangle(frame, (0, 0), (300, 60), (0,0,0), -1)
        cv2.putText(frame, f"{label}: {prob:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
    except Exception as e:
        print(f"Violence Process Error: {e}")
        
    return frame

# --- 4. VIDEO STREAMER CLASS ---

class VideoStreamer:
    def __init__(self):
        self.camera = None
        self.is_running = False
        self.mode = "weapon"
        self.current_source = None
        self.fps = 30 # Default FPS

    def start_stream(self, source=0, mode="weapon"):
        # Normalize Source
        if source == "webcam": source = 0
        if isinstance(source, str) and source.isdigit(): source = int(source)

        # Handle File Paths
        if isinstance(source, str):
            if not os.path.isabs(source):
                source = os.path.abspath(source)
            if not os.path.exists(source):
                print(f"❌ Error: File not found at {source}")
                return

        # Restart logic
        if self.is_running and self.camera:
            if self.current_source == source:
                self.mode = mode
                print(f"ℹ️ Stream running. Mode -> {mode}")
                return
            else:
                print(f"🔄 Switching source: {self.current_source} -> {source}")
                self.stop_stream()

        self.mode = mode
        self.current_source = source
        
        # Open Camera/File
        if os.name == 'nt' and (source == 0 or isinstance(source, int)):
            self.camera = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        else:
            self.camera = cv2.VideoCapture(source)

        if not self.camera.isOpened():
            print(f"❌ Critical Error: Could not open source {source}")
            self.is_running = False
        else:
            self.is_running = True
            # Get actual FPS from video file
            self.fps = self.camera.get(cv2.CAP_PROP_FPS)
            if self.fps <= 0 or self.fps > 120: self.fps = 30
            print(f"✅ Stream Started: {source} @ {self.fps:.2f} FPS")

    def stop_stream(self):
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None

    def generate_frames(self):
        # Calculate delay to match video FPS (e.g., 30fps -> 0.033s delay)
        frame_delay = 1.0 / self.fps if self.fps > 0 else 0.03
        
        while self.is_running and self.camera:
            start_time = time.time()
            
            success, frame = self.camera.read()
            if not success:
                # Loop video
                self.camera.set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, frame = self.camera.read()
                if not success:
                    self.stop_stream()
                    break

            try:
                if self.mode == "weapon":
                    processed_frame = process_weapon_frame(frame)
                elif self.mode == "violence":
                    processed_frame = process_violence_frame(frame)
                else:
                    processed_frame = frame

                ret, buffer = cv2.imencode('.jpg', processed_frame)
                if not ret: continue
                
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
                # 🛑 SPEED CONTROL: Sleep to match FPS
                process_time = time.time() - start_time
                wait_time = frame_delay - process_time
                if wait_time > 0:
                    time.sleep(wait_time)
                    
            except Exception as e:
                print(f"⚠️ Frame Error: {e}")
                continue

video_service = VideoStreamer()