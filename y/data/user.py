import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.String,
                           primary_key=True, unique=True)  # уникальный id. Предлагаю использовать uuid
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    creation_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)  # дата создания профиля, если она нужна
    #  posts = orm.relationship("Posts", back_populates='user')
