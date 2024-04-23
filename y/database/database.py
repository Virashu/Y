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


def create_post(username, text, is_answer=False, answer_to=None):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    if user:
        post = Posts()
        post.id = str(uuid.uuid4())
        post.author = user.username
        post.text = text
        post.is_answer = is_answer
        post.answer_to = answer_to
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


def dict_from_post(post):
    return {"id": post.id,
            "author": post.author,
            "text": post.text,
            "creation_time": post.creation_time,
            "editing_time": post.editing_time,
            "is_answer": post.is_answer,
            "answer_to": post.answer_to,
            "user_display_name": post.user.display_name}


def get_all_posts():
    db_sess = db_session.create_session()
    res = []
    for post in db_sess.query(Posts).filter(Posts.is_answer == False).all():
        res.append(dict_from_post(post))
    return res


def get_post_by_id(post_id):
    db_sess = db_session.create_session()
    post = db_sess.query(Posts).filter(Posts.id == post_id).first()
    return dict_from_post(post)


def get_posts_by_user(username):
    db_sess = db_session.create_session()
    res = []
    for post in db_sess.query(Posts).filter(Posts.author == username).filter(Posts.is_answer == False).all():
        res.append(dict_from_post(post))
    return res


def login_user(username: str, password: str) -> User | None:
    """Returns logged user or None"""

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    if user and user.hashed_password.__str__() == password:
        return user


def get_answers_to_post(post_id):
    db_sess = db_session.create_session()
    res = []
    for post in db_sess.query(Posts).filter(Posts.answer_to == post_id).all():
        res.append(dict_from_post(post))
    return res