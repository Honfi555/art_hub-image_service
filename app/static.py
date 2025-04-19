import dotenv
import os

dotenv.load_dotenv(".env")

SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")
REDIS_HOST: str = os.getenv("REDIS_HOST")
REDIS_PORT: int = int(os.getenv("REDIS_PORT")) if isinstance(os.getenv("REDIS_PORT"), str) else 6379
REDIS_DB: int = int(os.getenv("REDIS_DB")) if isinstance(os.getenv("REDIS_DB"), str) else 0
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
REDIS_USER: str = os.getenv("REDIS_USER")

IMAGE_CONTENT_TYPE: str = "image/jpeg"
