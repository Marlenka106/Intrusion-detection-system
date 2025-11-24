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
- DeepSORT (`deep-sort-realtime`)

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-логин/intrusion-detection-system.git
   cd intrusion-detection-system

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt  # включает deep-sort-realtime

## Запуск
Поместите видео (например, sample_video.mp4) в папку assets/, затем выполните:
   ```bash
   python -m src.main --video assets/sample_video.mp4   

Первый запуск: 
Если файл config/restricted_zones.json отсутствует, программа автоматически перейдёт в режим разметки:

Левый клик мыши — добавить точку полигона
s — сохранить текущую зону
n — начать новую зону
q — завершить разметку и начать детекцию
После завершения работы видео с наложенной тревогой будет сохранено в output/alarmed_video.mp4.
```