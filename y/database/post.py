import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = "posts"

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, unique=True)
    author = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("users.username")
    )
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    creation_time = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
    editing_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_answer = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    answer_to = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relationship("User")
