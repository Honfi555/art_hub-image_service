from logging import Logger
from typing import List
import base64
import uuid

from .connect import connect_redis
from ..logger import configure_logs
from ..models.articles import ImagesAdd

__all__: List[str] = ["insert_images", "delete_images", "select_article_images", "get_image_bytes"]

logger: Logger = configure_logs(__name__)

# Префиксы ключей в Redis
IMAGE_KEY_PREFIX: str = "image:"
ARTICLE_IMAGES_LIST: str = "article:{article_id}:images"
IMAGE_KEY: str = "image:{article_id}:{image_id}"

# Базовый URL для отдачи изображений
IMAGE_BASE_URL: str = "/images/"


def insert_images(images_data: ImagesAdd) -> List[str]:
	"""
	Вставляет изображения в Redis и сохраняет связь с соответствующей статьей.

	Для каждого изображения:
	- Декодирует base64 строку в байты.
	- Генерирует уникальный image_id.
	- Сохраняет байты изображения по ключу image:{article_id}:{image_id}.
	- Добавляет image_id в список article:{article_id}:images.

	:param images_data: Объект с идентификатором статьи и списком изображений в формате base64.
	:return: Список сгенерированных image_id для дальнейшего формирования URL.
	"""
	redis_client = connect_redis()
	article_id = images_data.article_id
	image_ids: List[str] = []
	for b64 in images_data.images:
		# Декодирование изображения из base64
		img_bytes = base64.b64decode(b64)
		# Генерация уникального идентификатора для изображения
		image_id = str(uuid.uuid4())
		key = f"image:{article_id}:{image_id}"
		# Сохранение байтов изображения в Redis
		redis_client.set(key, img_bytes)
		# Добавление идентификатора изображения в список статьи
		list_key = f"article:{article_id}:images"
		redis_client.rpush(list_key, image_id)
		image_ids.append(image_id)
	logger.info("Redis: вставлено %d изображений для статьи %s", len(image_ids), article_id)
	return image_ids


def delete_images(article_id: int, image_ids: List[str]) -> List[str]:
	"""
	Удаляет указанные изображения для данной статьи.

	Для каждого image_id:
	- Удаляет ключ image:{article_id}:{image_id} из Redis.
	- Убирает image_id из списка article:{article_id}:images.

	:param article_id: Идентификатор статьи, из которой удаляются изображения.
	:param image_ids: Список идентификаторов изображений для удаления.
	:return: Список удалённых идентификаторов изображений.
	"""
	logger.info("Удаление %d изображений для статьи %s", len(image_ids), article_id)
	client = connect_redis()
	list_key = ARTICLE_IMAGES_LIST.format(article_id=article_id)
	deleted: List[str] = []

	for image_id in image_ids:
		key = IMAGE_KEY.format(article_id=article_id, image_id=image_id)
		# Попытка удаления ключа
		if client.delete(key):
			# Если ключ был, то удаляем UID из списка
			client.lrem(list_key, 0, image_id)
			deleted.append(image_id)

	logger.info("Удалено %d изображений для статьи %s", len(deleted), article_id)
	return deleted


def select_article_images(article_id: int, announce: bool = False) -> List[str]:
	"""
	Получить список image_id для статьи.
	Если announce=True — вернуть только первый image_id, иначе все.
	"""
	redis_client = connect_redis()
	list_key = f"article:{article_id}:images"
	if announce:
		raw_ids = redis_client.lrange(list_key, 0, 0)
	else:
		raw_ids = redis_client.lrange(list_key, 0, -1)
	image_ids = [rid.decode('utf-8') for rid in raw_ids]
	logger.info("Redis: получено %d image_id для статьи %s (announce=%s)", len(image_ids), article_id, announce)
	return image_ids


def get_image_bytes(article_id: int, image_id: str) -> bytes | None:
	"""Получить байты изображения по article_id и image_id"""
	redis_client = connect_redis()
	key = f"image:{article_id}:{image_id}"
	data = redis_client.get(key)
	if data is None:
		logger.error("Redis: изображение не найдено: %s", key)
	return data
