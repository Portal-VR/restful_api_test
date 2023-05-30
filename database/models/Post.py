from database.SqlAlchemyDatabase import SqlAlchemyBase
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy_serializer import SerializerMixin


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(Text(1000), nullable=False)
    description = Column(String(100), nullable=False)

    def __init__(self, id: int, title: str, description: str, **kwargs):
        super().__init__()
        self.id = id
        self.title = title
        self.description = description

    def __repr__(self) -> str:
        return str(self.to_dict())
