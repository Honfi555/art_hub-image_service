from logging import Logger
import redis

from app.logger import configure_logs
from app.static import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, REDIS_USER

logger: Logger = configure_logs(__name__)


def connect_redis() -> redis.Redis:
    try:
        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            username=REDIS_USER,
            decode_responses=False
        )
        # Проверяем соединение
        r.ping()
        logger.info("Подключение к Redis успешно.")
        return r
    except Exception as e:
        logger.error("Ошибка подключения к Redis: %s", e)
        raise
