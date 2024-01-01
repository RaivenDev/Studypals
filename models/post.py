# Lidar com datas
from datetime import datetime

# Criar tabela
from factory import db

from pydantic import BaseModel

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.UnicodeText)
    #subject = db.Column(db.String(64), nullable=False, index=True)
    #done = db.Column(db.Boolean)
    schedule = db.Column(db.DateTime, default=datetime.utcnow)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"<Post {self.id}>"
    
from utils.responses import OrmBase

class PostCreate(BaseModel):
    text: str

from models.user import UserResponseSimple

class PostResponse(OrmBase):
    text: str
    #subject: str
    #done: bool
    schedule: datetime
    created: datetime
    author: UserResponseSimple


from typing import List

class PostResponseList(BaseModel):
    page: int
    pages: int
    total: int
    posts: List[PostResponse]

