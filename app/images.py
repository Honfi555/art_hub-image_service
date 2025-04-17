from logging import Logger

from .connect import connect_redis
from .logger import configure_logs

__all__ = ["select_article_images", "get_image_bytes"]
logger: Logger = configure_logs(__name__)
redis_client = connect_redis()

# Префиксы ключей в Redis
IMAGE_KEY_PREFIX = "image:"
ARTICLE_IMAGES_LIST = "article:{article_id}:images"

# Базовый URL для отдачи изображений
IMAGE_BASE_URL = "/images/"


def select_article_images(article_id: int, announce: bool = False) -> list[str]:
	"""
	Получить список image_id для статьи.
	Если announce=True — вернуть только первый image_id, иначе все.
	"""
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
	key = f"image:{article_id}:{image_id}"
	data = redis_client.get(key)
	if data is None:
		logger.error("Redis: изображение не найдено: %s", key)
	return data
