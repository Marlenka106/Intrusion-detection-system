# src/detector.py
from ultralytics import YOLO
import cv2

class YoloPersonDetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.5):
        """
        Инициализация детектора людей с YOLOv8.
        model_path: путь к модели (можно 'yolov8n.pt', 'yolov8s.pt' и т.д.)
        conf_threshold: порог уверенности для детекции
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.device = "cuda" if cv2.cuda.getCudaEnabledDeviceCount() > 0 else "cpu"
        print(f"YOLO загружен на устройстве: {self.device}")

    def detect(self, frame):
        """
        Детекция людей на кадре.
        Возвращает список: [{'bbox': (x1, y1, x2, y2), 'conf': float}, ...]
        """
        results = self.model(frame, classes=[0], conf=self.conf_threshold, device=self.device, verbose=False)
        detections = []
        for r in results[0].boxes:
            x1, y1, x2, y2 = map(int, r.xyxy[0])
            conf = float(r.conf[0])
            detections.append({
                'bbox': (x1, y1, x2, y2),
                'conf': conf
            })
        return detections

    def draw_detections(self, frame, detections):
        """Отрисовка bounding boxes на кадре."""
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"person {det['conf']:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame