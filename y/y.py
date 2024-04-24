import flask
import flask_login
import pathlib

from .database import db_session
from .database.user import User
from .database import database

from .forms import LoginForm, SignupForm, CreatePostForm, EditProfileForm

ROOT = str(pathlib.Path(__file__).parent.parent.resolve())  # Path of the project

app = flask.Flask(__name__, template_folder=f"{ROOT}/templates")

app.config["SECRET_KEY"] = "huh"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


pages = ["index", "signup", "login", "profile"]


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        request = flask.request.form.keys()
        for r in request:
            return flask.redirect(f"/comments?post_id={r}&back=")
    user = flask_login.current_user
    posts = database.get_all_posts()
    return flask.render_template("index.html", pages=pages, user=user,
                                 posts=posts[::-1])


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = database.create_user(
            form.username.data,
            form.display_name.data,
            form.email.data,
            form.password.data,
        )
        if user:
            if flask_login.login_user(user, remember=form.remember_me.data):
                return flask.redirect("/")

        return flask.render_template(
            "signup.html",
            message="Error",
            form=form,
            pages=pages,
            is_logged_in=False,
        )
    return flask.render_template(
        "signup.html", pages=pages, form=form, is_logged_in=False
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = database.login_user(form.username.data, form.password.data)
        if user:
            flask_login.login_user(user, remember=form.remember_me.data)
            return flask.redirect("/")
        return flask.render_template(
            "login.html",
            message="Неправильный логин или пароль",
            form=form,
            pages=pages,
            user=user,
        )
    return flask.render_template("login.html", pages=pages, form=form, user=None)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if flask.request.method == "POST":
        if "create" in flask.request.form:
            return flask.redirect("/create-post")
        elif "edit-profile" in flask.request.form:
            return flask.redirect("/edit-profile")
        else:
            request = flask.request.form.values()
            if "comments" in flask.request.form:
                for r in request:
                    return flask.redirect(f"/comments?post_id={r}&back=profile")
            elif "edit" in flask.request.form:
                for r in request:
                    return flask.redirect(f"/edit-post?post_id={r}")
            else:
                for r in request:
                    database.delete_post(r)
                    return flask.redirect(f"/profile")

    username = flask.request.args.get("u", None)
    if username:
        user = (
            db_session.create_session()
            .query(User)
            .filter(User.username == username)
            .first()
        )
    else:
        user = flask_login.current_user
        if not user or user.__class__ is flask_login.mixins.AnonymousUserMixin:
            return flask.redirect("/login")
    posts = database.get_posts_by_user(user.username)
    return flask.render_template("profile.html", pages=pages, user=user, posts=posts[::-1])


@app.route("/create-post", methods=["GET", "POST"])
def create_post():
    form = CreatePostForm()
    if form.submit.data:
        username = flask.request.args.get("u", None)
        if username:
            user = (
                db_session.create_session()
                .query(User)
                .filter(User.username == username)
                .first()
            )
        else:
            user = flask_login.current_user
            if not user:
                return flask.redirect("/login")
        if "answer_to" not in flask.request.url:
            post = database.create_post(user.username, form.text.data)
            return flask.redirect("/profile")
        else:
            a = flask.request.values["answer_to"]
            back = flask.request.values["back"]
            post = database.create_post(user.username, form.text.data,
                                        is_answer=True, answer_to=a)
            return flask.redirect(f"/comments?post_id={a}&back={back}")
    if form.cancel.data:
        return flask.redirect("/profile")
    return flask.render_template("create_post.html", pages=pages, form=form)


@app.route("/edit-post", methods=["GET", "POST"])
def edit_post():
    form = CreatePostForm()
    if form.submit.data:
        username = flask.request.args.get("u", None)
        if username:
            user = (
                db_session.create_session()
                .query(User)
                .filter(User.username == username)
                .first()
            )
        else:
            user = flask_login.current_user
            if not user:
                return flask.redirect("/login")
        database.edit_post(flask.request.values["post_id"], form.text.data)
        return flask.redirect("/profile")
    if form.cancel.data:
        return flask.redirect("/profile")
    post = database.get_post_by_id(flask.request.values["post_id"])
    form.text.data = post["text"]
    return flask.render_template("create_post.html", pages=pages, form=form)


@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    form = EditProfileForm()
    username = flask.request.args.get("u", None)
    if username:
        user = (
            db_session.create_session()
            .query(User)
            .filter(User.username == username)
            .first()
        )
    else:
        user = flask_login.current_user
        if not user:
            return flask.redirect("/login")
    if form.submit.data:
        database.edit_user(form.username.data, form.display_name.data,
                           form.description.data, form.email.data, form.password.data)
        return flask.redirect("/profile")
    if form.cancel.data:
        return flask.redirect("/profile")
    form.username.data = user.username
    form.email.data = user.email
    form.display_name.data = user.display_name
    form.description.data = user.description
    return flask.render_template("edit_profile.html", pages=pages, form=form)


@app.route("/comments", methods=["GET", "POST"])
def comments_to_post():
    if flask.request.method == "POST":
        if "answer" in flask.request.form:
            return flask.redirect(f"/create-post?answer_to={flask.request.values['post_id']}")
        else:
            return flask.redirect(f"/{flask.request.values['back']}")
    username = flask.request.args.get("u", None)
    if username:
        user = (
            db_session.create_session()
            .query(User)
            .filter(User.username == username)
            .first()
        )
    else:
        user = flask_login.current_user
        if not user:
            return flask.redirect("/login")
    id = flask.request.values["post_id"]
    post = database.get_post_by_id(id)
    comments = database.get_answers_to_post(id)
    return flask.render_template("post_with_comments.html", pages=pages, user=user,
                                 post=post, comments=comments)