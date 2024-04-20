import datetime

import sqlalchemy

from .db_session import SqlAlchemyBase
import flask_login


class User(SqlAlchemyBase, flask_login.UserMixin):
    __tablename__ = "users"

    username = sqlalchemy.Column(sqlalchemy.String, primary_key=True, unique=True)
    display_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    creation_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
    posts = sqlalchemy.orm.relationship("Posts", back_populates='user')

    def get_id(self):
        return str(self.username)
