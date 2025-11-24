# Intrusion Detection System

Система отслеживания проникновения на запрещённую территорию с использованием YOLO и OpenCV.

## Основные возможности
- Детекция людей с помощью YOLOv8
- Трекинг людей с помощью DeepSORT (уникальные ID)
- Интерактивная разметка запрещённых зон поверх видео
- Автоматическое сохранение и загрузка зон из `config/restricted_zones.json`
- Визуальная тревога ("ALARM!") при проникновении
- Автоматическое отключение тревоги через 3 секунды после выхода из зоны
- Автоматическая запись видео с тревогой в папку output/

## Требования
- Python 3.11+
- OpenCV
- YOLOv8 (ultralytics)

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-логин/intrusion-detection-system.git
   cd intrusion-detection-system

2. ```bash
   pip install -r requirements.txt  # включает deep-sort-realtime

## Запуск

```bash
python -m src.main --video assets/sample_video.mp4   

