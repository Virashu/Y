import uuid
from typing import Optional, Any

from . import db_session
from .post import Post
from .user import User

# db_session.global_init("db/y.db")


def create_user(username, display_name, email, hashed_password) -> User | None:
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

    # return user


def create_post(
    username: str, text: str, is_answer: bool = False, answer_to: Optional[str] = None
) -> Post | None:
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    if user:
        post = Post(
            id=str(uuid.uuid4()),
            author=user.username,
            text=text,
            is_answer=is_answer,
            answer_to=answer_to,
        )

        db_sess.add(post)
        db_sess.commit()

        return post

    return None


def edit_user(username, name, description, email, hashed_password) -> None:
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()

    user.display_name = name
    user.description = description
    user.email = email
    user.hashed_password = hashed_password

    db_sess.commit()


def edit_post(post_id: str, text: str) -> None:
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == post_id).first()
    post.text = text
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


# Typing nightmare >:(
def dict_from_post(post: Post) -> dict[str, Any]:
    return {
        "id": post.id,
        "author": post.author,
        "text": post.text,
        "creation_time": post.creation_time,
        "editing_time": post.editing_time,
        "is_answer": post.is_answer,
        "answer_to": post.answer_to,
        "user_display_name": post.user.display_name,
    }


def get_all_posts() -> list[Post]:
    db_sess = db_session.create_session()
    # Why map to dict tho?
    return db_sess.query(Post).filter(Post.is_answer == False).all()


def get_post_by_id(post_id) -> Post | None:
    db_sess = db_session.create_session()
    return db_sess.query(Post).filter(Post.id == post_id).first()


def get_posts_by_user(username) -> list[Post]:
    db_sess = db_session.create_session()
    return (
        db_sess.query(Post)
        .filter(Post.author == username)
        .filter(Post.is_answer == False)
        .all()
    )


def login_user(username: str, password: str) -> User | None:
    """Returns logged user or None"""

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    if user and user.hashed_password.__str__() == password:
        return user


def get_answers_to_post(post_id) -> list[Post]:
    db_sess = db_session.create_session()
    return db_sess.query(Post).filter(Post.answer_to == post_id).all()


def reaction_to_post(post_id, username) -> None:
    db_sess = db_session.create_session()
    post: Post | None = db_sess.query(Post).filter(Post.id == post_id).first()
    if username not in post.reacted_users:
        post.reactions += 1
        post.reacted_users += username
        db_sess.commit()
