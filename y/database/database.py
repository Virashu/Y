from . import db_session
from .post import Posts
from .user import User
import uuid

db_session.global_init("db/y.db")


def create_user(username, display_name, email, hashed_password) -> User | None:
    db_sess = db_session.create_session()

    if db_sess.query(User).filter(User.username == username).first():
        return None  # User already exists

    user = User()

    user.username = username
    user.display_name = display_name
    user.email = email
    user.hashed_password = hashed_password

    db_sess.add(user)
    db_sess.commit()

    return user


def create_post(username, text):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    if user:
        post = Posts()
        post.id = str(uuid.uuid4())
        post.author = user.username
        post.text = text
        db_sess.add(post)
        db_sess.commit()
    else:
        return None
    return post


def edit_user(username, name, description, email, hashed_password):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    user.display_name = name
    user.description = description
    user.email = email
    user.hashed_password = hashed_password

    db_sess.commit()


def edit_post(): ...


def delete_user(username: str):
    db_sess = db_session.create_session()
    db_sess.query(User).filter(User.username == username).delete()
    db_sess.commit()


def delete_post(): ...


def get_all_users():
    db_sess = db_session.create_session()
    res = []
    for user in db_sess.query(User).all():
        res.append(user)
    return res


def get_user_by_username(username: str):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    return user


def get_all_posts():
    db_sess = db_session.create_session()
    res = []
    for post in db_sess.query(Posts).all():
        res.append(post)
    return res


def get_post_by_id(): ...


def login_user(username: str, password: str) -> User | None:
    """Returns logged user or None"""

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    if user and user.hashed_password.__str__() == password:
        return user
