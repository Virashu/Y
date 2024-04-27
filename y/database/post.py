import datetime

import sqlalchemy as sql
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = "posts"

    id = sql.Column(sql.String, primary_key=True, unique=True)
    author = sql.Column(sql.String, sql.ForeignKey("users.username"))
    text = sql.Column(sql.String)
    creation_time = sql.Column(sql.DateTime, default=datetime.datetime.now)
    editing_time = sql.Column(sql.DateTime, default=datetime.datetime.now)
    answer_to = sql.Column(sql.String, nullable=True)
    reactions = sql.Column(sql.Integer, default=0)
    reacted_users = sql.Column(sql.String, default="")
    user = orm.relationship("User", lazy="joined")
