# src/zone_checker.py
import cv2
import numpy as np
from typing import List, Tuple

def is_point_in_any_zone(point: Tuple[int, int], zones: List[dict]) -> bool:
    """
    Проверяет, находится ли точка (x, y) внутри хотя бы одной из запрещённых зон.
    
    :param point: (x, y)
    :param zones: список зон в формате [{"points": [[x1,y1], [x2,y2], ...]}, ...]
    :return: True, если точка в зоне
    """
    for zone in zones:
        points = np.array(zone["points"], dtype=np.int32)
        """ 
        cv2.pointPolygonTest(..., measureDist=False) → возвращает:
                > 0 — внутри
                = 0 — на границе
                < 0 — снаружи
                Мы считаем внутри ИЛИ на границе за проникновение → >= 0
        """
        if cv2.pointPolygonTest(points, point, False) >= 0:
            return True
    return False

def draw_zones(frame, zones):
    """Отрисовка запрещённых зон как замкнутых полигонов."""
    for zone in zones:
        points = np.array(zone["points"], dtype=np.int32)
        cv2.polylines(frame, [points], isClosed=True, color=(0, 0, 255), thickness=2)
    return frame