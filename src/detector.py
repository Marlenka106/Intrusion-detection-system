# src/detector.py (обновлённая версия)
from ultralytics import YOLO
import cv2

class YoloPersonDetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.5):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.device = "cuda" if cv2.cuda.getCudaEnabledDeviceCount() > 0 else "cpu"
        print(f"YOLO загружен на устройстве: {self.device}")

    def detect(self, frame):
        results = self.model(frame, classes=[0], conf=self.conf_threshold, device=self.device, verbose=False)
        detections = []
        for r in results[0].boxes:
            x1, y1, x2, y2 = map(int, r.xyxy[0])
            conf = float(r.conf[0])
            detections.append({'bbox': (x1, y1, x2, y2), 'conf': conf})
        return detections