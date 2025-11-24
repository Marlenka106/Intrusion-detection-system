# src/main.py
import argparse
import os
import json
import cv2
from src.detector import YoloPersonDetector
from src.zone_checker import is_point_in_any_zone, draw_zones
import time

CONFIG_PATH = "config/restricted_zones.json"


def load_zones():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return []


def annotation_mode(video_path):
    """
    Режим разметки: пользователь кликает, чтобы задать точки зоны.
    """
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Не удалось прочитать видео")
        return

    zones = []
    current_polygon = []

    def mouse_callback(event, x, y, flags, param):
        nonlocal current_polygon
        if event == cv2.EVENT_LBUTTONDOWN:
            current_polygon.append((x, y))
            print(f"Добавлена точка: ({x}, {y})")

    cv2.namedWindow("Annotation Mode")
    cv2.setMouseCallback("Annotation Mode", mouse_callback)

    print("Инструкция:")
    print("- ЛКМ: добавить точку полигона")
    print("- Нажмите 's', чтобы сохранить текущую зону")
    print("- Нажмите 'n', чтобы начать новую зону")
    print("- Нажмите 'q', чтобы завершить и сохранить все зоны")

    while True:
        display_frame = frame.copy()

        # Отрисовка текущего полигона
        for i, point in enumerate(current_polygon):
            cv2.circle(display_frame, point, 5, (0, 255, 0), -1)
            if i > 0:
                cv2.line(display_frame, current_polygon[i - 1], point, (0, 255, 0), 2)

        cv2.imshow("Annotation Mode", display_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            if len(current_polygon) >= 3:
                zones.append({"points": current_polygon.copy()})
                print(f"Зона сохранена. Всего зон: {len(zones)}")
            else:
                print("Зона должна содержать минимум 3 точки!")

        elif key == ord("n"):
            current_polygon.clear()
            print("Начата новая зона")

        elif key == ord("q"):
            break

    cv2.destroyAllWindows()

    if zones:
        os.makedirs("config", exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(zones, f, indent=4)
        print(f"Зоны сохранены в {CONFIG_PATH}")
    else:
        print("Нет сохранённых зон.")


def detection_mode(video_path):
    print("Запуск режима детекции с проверкой проникновения...")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Не удалось открыть видео")
        return

    zones = load_zones()
    if not zones:
        print("Нет запрещённых зон. Запустите разметку.")
        return

    detector = YoloPersonDetector()
    alarm_active = False
    last_seen_in_zone_time = 0

    cv2.namedWindow("Intrusion Detection", cv2.WND_PROP_AUTOSIZE)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        detections = detector.detect(frame)
        someone_in_zone = False

        # Проверка проникновения
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            if is_point_in_any_zone(center, zones):
                someone_in_zone = True
                last_seen_in_zone_time = current_time
                # Опционально: подсветить человека в зоне красным
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Логика тревоги
        if someone_in_zone:
            alarm_active = True
        elif alarm_active and (current_time - last_seen_in_zone_time) >= 3.0:
            alarm_active = False

        # Отрисовка
        frame = draw_zones(frame, zones)
        if alarm_active:
            cv2.putText(frame, "ALARM!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        cv2.imshow("Intrusion Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Путь к видеофайлу")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"Видеофайл не найден: {args.video}")
        return

    zones = load_zones()
    if not zones:
        print("Файл зон не найден — запускаем режим разметки")
        annotation_mode(args.video)
    else:
        print(f"Найдено {len(zones)} запрещённых зон — запускаем детекцию")
        detection_mode(args.video)


if __name__ == "__main__":
    main()