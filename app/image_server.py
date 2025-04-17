from fastapi import FastAPI, HTTPException, Response
from .images import select_article_images, get_image_bytes

app = FastAPI()


@app.get("/images/{article_id}")
async def list_images(article_id: int, announce: bool = False):
	ids = select_article_images(article_id, announce)
	if not ids:
		raise HTTPException(status_code=404, detail="Images not found")
	# Возвращаем клиенту список URL
	return {"image_urls": [
		f"/image/{article_id}/{image_id}" for image_id in ids
	]}


@app.get("/image/{article_id}/{image_id}")
async def fetch_image(article_id: int, image_id: str):
	data = get_image_bytes(article_id, image_id)
	if not data:
		raise HTTPException(status_code=404, detail="Image not found")
	return Response(content=data, media_type="image/jpeg")
