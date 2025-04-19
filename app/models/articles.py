from pydantic import BaseModel

__all__: list[str] = ["ImagesAdd"]


class ImagesAdd(BaseModel):
	article_id: int
	images: list[str]
