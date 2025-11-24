# src/main.py
import argparse
import os
import json
import cv2
from src.detector import YoloPersonDetector
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
    print("Запуск режима детекции с YOLO...")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Не удалось открыть видео")
        return

    detector = YoloPersonDetector()

    cv2.namedWindow("Intrusion Detection", cv2.WND_PROP_FULLSCREEN)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Детекция людей
        detections = detector.detect(frame)
        frame = detector.draw_detections(frame, detections)

        # ПОКА НЕТ ПРОВЕРКИ ЗОН И ТРЕВОГИ — добавим в следующем шаге

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