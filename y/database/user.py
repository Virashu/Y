import datetime

import sqlalchemy as sql

from .db_session import SqlAlchemyBase
import flask_login


class User(SqlAlchemyBase, flask_login.UserMixin):
    __tablename__ = "users"

    username = sql.Column(sql.String, primary_key=True, unique=True)
    display_name = sql.Column(sql.String, nullable=True)
    description = sql.Column(sql.String, default="")
    email = sql.Column(sql.String, index=True, unique=True, nullable=True)
    hashed_password = sql.Column(sql.String, nullable=True)
    creation_date = sql.Column(sql.DateTime, default=datetime.datetime.now)
    posts = sql.orm.relationship("Post", back_populates="user")

    def get_id(self):
        return str(self.username)
