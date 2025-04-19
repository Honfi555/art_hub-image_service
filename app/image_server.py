from fastapi import FastAPI, HTTPException, Response, status, Query, Body, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .dependecies import verify_jwt
from .models.articles import ImagesAdd
from .database.images import select_article_images, get_image_bytes, insert_images, delete_images

app = FastAPI()

# Разрешить CORS для любых Origin, заголовков и методов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # любые домены/IP
    allow_credentials=True,
    allow_methods=["*"],            # любые HTTP‑методы
    allow_headers=["*"],            # любые заголовки
)


@app.delete("/remove_images")
@verify_jwt
async def remove_article_images(
	article_id: int = Query(..., description="ID статьи"),
	image_ids: list[str] = Body(..., description="Список ID изображений для удаления"),
	authorization: str = Header(...)
):
	"""
	Удаляет изображения, связанные со статьей.

	Параметры:
		article_id (int): ID статьи.
		image_ids (list[str]): Список идентификаторов изображений для удаления.
		authorization (str): Токен авторизации, передаваемый в заголовке.

	Возвращает:
		JSONResponse: Статус операции и список удалённых идентификаторов изображений.

	Исключения:
		HTTPException: 500, если происходит ошибка на сервере.
	"""
	try:
		# delete_images теперь принимает article_id и список UUID строк
		deleted = delete_images(article_id, image_ids)
		return JSONResponse(
			status_code=status.HTTP_200_OK,
			content={"deleted_image_ids": deleted}
		)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=str(e)
		)


@app.put("/add_images")
@verify_jwt
async def add_article_images(
	article_id: int = Query(..., description="ID статьи"),
	images: list[str] = Body(..., description="Список base64-строк или URL файлов для вставки"),
	authorization: str = Header(...)
):
	"""
	Добавляет изображения к статье.

	Параметры:
		article_id (int): ID статьи.
		images (list[str]): Список изображений, представленных в виде base64-строк или URL файлов.
		authorization (str): Токен авторизации, передаваемый в заголовке.

	Возвращает:
		JSONResponse: Статус операции и список сгенерированных идентификаторов изображений.

	Исключения:
		HTTPException: 500, если происходит ошибка на сервере.
	"""
	try:
		# insert_images возвращает список сгенерированных UUID
		created = insert_images(ImagesAdd(article_id=article_id, images=images))
		return JSONResponse(
			status_code=status.HTTP_201_CREATED,
			content={"created_image_ids": created}
		)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=str(e)
		)


@app.get("/images/{article_id}")
@verify_jwt
async def list_images(article_id: int, authorization: str = Header(...), announce: bool = False):
	"""
	Получает список изображений, связанных со статьей.

	Параметры:
		article_id (int): ID статьи.
		authorization (str): Токен авторизации, передаваемый в заголовке.
		announce (bool): Флаг, влияющий на выбор изображений (по умолчанию False).

	Возвращает:
		dict: Словарь с ключом 'image_urls', содержащий список URL изображений.

	Исключения:
		HTTPException: 204, если изображения не найдены.
	"""
	ids = select_article_images(article_id, announce)
	if not ids:
		raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Images not found")
	# Возвращаем клиенту список URL
	return {"image_urls": [
		f"/image/{article_id}/{image_id}" for image_id in ids
	]}


@app.get("/image/{article_id}/{image_id}")
async def fetch_image(article_id: int, image_id: str):
	"""
	Получает изображение по идентификатору статьи и изображения.

	Параметры:
		article_id (int): ID статьи.
		image_id (str): Идентификатор изображения.
		authorization (str): Токен авторизации, передаваемый в заголовке.

	Возвращает:
		Response: Изображение в формате JPEG.

	Исключения:
		HTTPException: 204, если изображение не найдено.
	"""
	data = get_image_bytes(article_id, image_id)
	if not data:
		raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Images not found")
	return Response(content=data, media_type="image/jpeg")
