from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post(
    '/post',
    status_code=status.HTTP_200_OK,
    tags=['Post'],
    description='Создает сущность поста'
)
async def create_post():
    pass


