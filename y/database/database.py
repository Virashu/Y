import datetime
import uuid
from typing import Optional

from ..config import DB_PATH
from .db_session import SessionFactory
from .post import Post
from .user import User

db_session = SessionFactory(DB_PATH)


def create_user(
    username: str, display_name: str, email: str, hashed_password: str
) -> User | None:
    db_sess = db_session.create_session()

    if db_sess.query(User).filter(User.username == username).first():
        return None  # User already exists

    user = User(
        username=username,
        display_name=display_name,
        email=email,
        hashed_password=hashed_password,
    )

    db_sess.add(user)
    db_sess.commit()

    return user


def create_post(
    username: str, text: str, answer_to: Optional[str] = None
) -> Post | None:
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()

    if user is None:
        return None

    post = Post(
        id=str(uuid.uuid4()),
        author=user.username,
        text=text,
        answer_to=answer_to,
    )

    db_sess.add(post)
    db_sess.commit()

    return post


def edit_user(
    username: str, name: str, description: str, email: str, hashed_password: str
) -> None:
    db_sess = db_session.create_session()

    db_sess.query(User).filter(User.username == username).update(
        {
            "display_name": name,
            "description": description,
            "email": email,
            "hashed_password": hashed_password,
        }
    )

    db_sess.commit()


def edit_post(post_id: str, text: str) -> None:
    db_sess = db_session.create_session()
    (
        db_sess.query(Post)
        .filter(Post.id == post_id)
        .update({"text": text, "editing_time": datetime.datetime.now()})
    )
    db_sess.commit()


def delete_user(username: str) -> None:
    db_sess = db_session.create_session()
    db_sess.query(User).filter(User.username == username).delete()
    db_sess.commit()


def delete_post(post_id: str) -> None:
    db_sess = db_session.create_session()
    db_sess.query(Post).filter(Post.id == post_id).delete()
    db_sess.commit()


def get_all_users() -> list[User]:
    db_sess = db_session.create_session()
    return db_sess.query(User).all()


def get_user_by_username(username: str) -> User | None:
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    return user


def get_all_posts() -> list[Post]:
    db_sess = db_session.create_session()
    return (
        db_sess.query(Post)
        .filter(Post.answer_to.is_(None))
        .order_by(Post.creation_time.desc())
        .all()
    )


def get_post_by_id(post_id: str) -> Post | None:
    db_sess = db_session.create_session()
    return db_sess.query(Post).filter(Post.id == post_id).first()


def get_posts_by_user(username: str) -> list[Post]:
    db_sess = db_session.create_session()
    return (
        db_sess.query(Post)
        .filter(Post.author == username)
        .filter(Post.answer_to.is_(None))
        .all()
    )


def login_user(username: str, password: str) -> User | None:
    """Returns logged user or None"""

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()

    if user and str(user.hashed_password) == password:
        return user

    return None


def get_answers_to_post(post_id: str) -> list[Post]:
    db_sess = db_session.create_session()
    return (
        db_sess.query(Post)
        .filter(Post.answer_to == post_id)
        .order_by(Post.reactions.desc())
        .all()
    )


def reaction_to_post(post_id: str, username: str) -> None:
    db_sess = db_session.create_session()

    post_query = (
        db_sess.query(Post)
        .filter(Post.id == post_id)
        .filter(~Post.reacted_users.contains(username))
    )

    post = post_query.first()

    if not post:
        return

    post_query.update(
        {
            "reactions": post.reactions + 1,
            "reacted_users": post.reacted_users + username,
        }
    )

    db_sess.commit()
