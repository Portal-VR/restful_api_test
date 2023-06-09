from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

import config
from dotenv import load_dotenv
from os import environ
from time import sleep


def load_models():
    import database.models.Post


load_dotenv()  # load connection string from .env file
# create engin (echo for showing sql requests)
if environ.get("PRODUCTION") == "true":
    sleep(10)
engine: AsyncEngine = create_async_engine(config.DATABASE_URL)
SqlAlchemyBase = declarative_base()
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
load_models()


async def get_session() -> AsyncSession:
    """
    Create async session for work with database
    :return: AsyncSession
    """
    async with async_session_maker() as session:
        yield session


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SqlAlchemyBase.metadata.drop_all)
        await conn.run_sync(SqlAlchemyBase.metadata.create_all)
