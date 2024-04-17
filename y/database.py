from data import db_session
from data.user import User
from data.post import Posts
import uuid


db_session.global_init("db/y.db")


def create_user(name, email, hashed_password):
    user = User()
    user.id = str(uuid.uuid4())
    user.name = name
    user.email = email
    user.hashed_password = hashed_password
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def create_post():
    ...


def edit_user(id: str, name, description, email, hashed_password):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    user.name = name
    user.description = description
    user.email = email
    user.hashed_password = hashed_password

    db_sess.commit()


def edit_post():
    ...


def delete_user(id: str):
    db_sess = db_session.create_session()
    db_sess.query(User).filter(User.id == id).delete()
    db_sess.commit()


def delete_post():
    ...


def get_all_users():
    db_sess = db_session.create_session()
    res = []
    for user in db_sess.query(User).all():
        res.append(user)
    return res


def get_user_by_id(id: str):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    return user


def get_all_posts():
    ...


def get_post_by_id():
    ...
