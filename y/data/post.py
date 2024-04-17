import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Posts(SqlAlchemyBase):
    __tablename__ = "posts"

    id = sqlalchemy.Column(
        sqlalchemy.String, primary_key=True, unique=True
    )  # уникальный id. Предлагаю использовать uuid
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    creation_time = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
    editing_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_answer = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    answer_to = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    #  user = orm.relationship('User')
