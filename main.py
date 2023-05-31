import asyncio

import uvicorn
from fastapi import FastAPI, Depends
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from database.SqlAlchemyDatabase import init_models
from models import PostCreate
from models.models import PostUpdate
from services.posts import PostsService

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def app_root():
    return {
        "status": "ok",
        "message": "pong",
    }


@app.get(
    '/post',
    status_code=status.HTTP_200_OK,
    tags=['Post'],
    description='Получает список постов'
)
async def app_get_posts(
        posts_service: PostsService = Depends()
):
    """Getting post list"""
    return {"status": "ok", 'posts': await posts_service.get_many()}


@app.post(
    '/post',
    status_code=status.HTTP_201_CREATED,
    tags=['Post'],
    description='Создает сущность поста',
)
async def app_create_post(
        post: PostCreate,
        posts_service: PostsService = Depends()
):
    """Creating the post"""
    return {"status": "ok", 'post': await posts_service.create(post)}


@app.get(
    '/post/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Post'],
    description='Получает сущность поста'
)
async def app_get_post(id: int, posts_service: PostsService = Depends()):
    result = await posts_service.get(id)
    if result is None:
        return {"status": "error", "message": "No such post with provided id"}
    return {"status": "ok", "post": result}


@app.patch(
    '/post/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Post'],
    description='Получает сущность поста'
)
async def app_update_post(id: int, post: PostUpdate, posts_service: PostsService = Depends()):
    result = await posts_service.update(id, post)
    return {"status": "ok", "post": post}


@app.delete(
    '/post/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Post'],
    description='Удаляет пост'
)
async def app_delete_post(id: int, posts_service: PostsService = Depends()):
    if not await posts_service.delete(id):
        return {"status": "error", "message": "No such post with provided id"}
    return {"status": "ok", "message": "success"}


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
