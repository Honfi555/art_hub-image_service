# Проект Image Server

## Описание
Проект реализует HTTP API для управления изображениями, связанными со статьями. Используется FastAPI для создания REST API, Redis для хранения изображений и идентификаторов, а также Python в качестве языка разработки.

## Функциональность
- \*Удаление изображений\*: Эндпоинт для удаления изображений, связанных со статьёй.
- \*Добавление изображений\*: Эндпоинт для добавления изображений к статье, принимающий список base64-строк или URL файлов.
- \*Получение списка изображений\*: Эндпоинт для получения списка URL изображений, связанных со статьёй, с возможностью фильтрации.
- \*Получение изображения\*: Эндпоинт для получения конкретного изображения по article\_id и image\_id.

## Структура проекта
- `app/image_server.py` — основной файл с описанием API.
- `app/database/images.py` — модуль для работы с Redis, осуществляющий операции получения, добавления и удаления изображений.
- `app/dependecies.py` — модуль с зависимостями, например, функции для проверки JWT.
- `app/models/articles.py` — определение моделей данных (например, модель ImagesAdd).

## Установка и запуск
1. Клонируйте репозиторий:
   ```bash
   cd /opt
   git clne https://github.com/Honfi555/art_hub-image_service.git
   cd ./art_hub-image_service
   ```
2. Установка зависимостей
   ```bash
   python -m venv .venv
   source ./.venv/bin/activate
   pip install -r ./requirements.txt
   ```
3. Настройка папки логов (в случае размещения репозитория в /opt)
   ```bash
   sudo mkdir -p /opt/art_hub-image_service/logs
   sudo touch /opt/art_hub-image_service/logs/app.log
   sudo chown -R www-data:www-data /opt/art_hub-image_service/logs
   sudo chmod 755 /opt/art_hub-image_service/logs
   sudo chmod 644 /opt/art_hub-image_service/logs/app.log
   ```
4. Установка daemon
   ```bash
   cp ./image-server.service /etc/systemd/system/image-server.service
   systemctl daemon-reload
   ```
5. Запуск daemon
   ```bash
   systemctl start image-server.servise
   systemctl enable image-server.servise
   ```