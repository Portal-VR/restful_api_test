from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Post as SQLPost

from database.SqlAlchemyDatabase import get_session
from models import PostCreate
from models.models import PostUpdate


class PostsService:
    def __init__(self, db_session: AsyncSession = Depends(get_session)):
        self.db_session = db_session

    async def get_many(self):
        stmt_get_post_list = select(SQLPost)
        query_post_list: ChunkedIteratorResult = await self.db_session.execute(stmt_get_post_list)
        post_list = query_post_list.fetchall()
        print(post_list)
        return post_list

    async def get(self, post_id: int):
        stmt_get_post = select(SQLPost).where(
            SQLPost.id == post_id
        )
        post_with_such_id = (await self.db_session.execute(stmt_get_post)).all()
        if len(post_with_such_id) == 0:
            return None
        return post_with_such_id[0][0]

    async def create(self, post: PostCreate):
        post_in_db = PostCreate(
            title=post.title,
            description=post.description
        )
        post_model = SQLPost(**post_in_db.dict())
        self.db_session.add(post_model)
        await self.db_session.commit()
        return post

    async def update(
            self,
            post_id: int,
            post: PostUpdate
    ):
        stmt_get_post = select(SQLPost).where(
            SQLPost.id == post_id
        )
        post_with_such_id = (await self.db_session.execute(stmt_get_post)).all()
        if len(post_with_such_id) == 0:
            return False
        await self.db_session.execute(
            update(SQLPost)
            .where(SQLPost.id == post_id)
            .values(**dict(post))
        )
        await self.db_session.commit()

    async def delete(self, post_id: int):
        stmt_get_post = select(SQLPost).where(
            SQLPost.id == post_id
        )
        post_with_such_id = (await self.db_session.execute(stmt_get_post)).all()
        if len(post_with_such_id) == 0:
            return False
        await self.db_session.delete(post_with_such_id[0][0])
        await self.db_session.commit()
        return True
