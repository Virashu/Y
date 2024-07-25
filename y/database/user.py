import datetime
from typing import override

import flask_login
import sqlalchemy as sql

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, flask_login.UserMixin):
    __tablename__ = "users"

    username = sql.Column(sql.String, primary_key=True, unique=True)
    display_name = sql.Column(sql.String, nullable=True)
    description = sql.Column(sql.String, default="")
    email = sql.Column(sql.String, index=True, unique=True, nullable=True)
    hashed_password = sql.Column(sql.String)
    creation_date = sql.Column(sql.DateTime, default=datetime.datetime.now)
    salt = sql.Column(sql.String)
    posts = sql.orm.relationship("Post", back_populates="user")

    @override
    def get_id(self):
        return str(self.username)
