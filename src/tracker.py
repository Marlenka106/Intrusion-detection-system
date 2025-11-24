# src/tracker.py
from ultralytics.utils.ops import xyxy2xywh
from deep_sort_realtime.deepsort_tracker import DeepSort
import numpy as np

class DeepSortTracker:
    def __init__(self, max_age=30, n_init=3, max_iou_distance=0.7):
        self.tracker = DeepSort(
            max_age=max_age,
            n_init=n_init,
            max_iou_distance=max_iou_distance,
            embedder="mobilenet"
        )

    def update(self, detections, frame):
        """
        Обновление треков.
        :param detections: список {'bbox': (x1,y1,x2,y2), 'conf': float}
        :param frame: текущий кадр (numpy array)
        :return: список {'track_id': int, 'bbox': (x1,y1,x2,y2), 'in_zone': bool}
        """
        bbs = []
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            w, h = x2 - x1, y2 - y1
            bbs.append(([x1, y1, w, h], det['conf'], 'person'))

        if not bbs:
            return []

        # Передаём frame для вычисления эмбеддингов
        tracks = self.tracker.update_tracks(bbs, frame=frame)

        result = []
        for track in tracks:
            if not track.is_confirmed():
                continue
            ltrb = track.to_ltrb()
            result.append({
                'track_id': track.track_id,
                'bbox': tuple(map(int, ltrb)),
                'in_zone': False
            })
        return result