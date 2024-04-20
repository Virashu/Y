import flask
import flask_login
import pathlib

from .database import db_session
from .database.user import User
from .database import database

from .forms import LoginForm, SignupForm, CreatePostForm

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
    user = flask_login.current_user

    return flask.render_template("index.html", pages=pages, user=user)


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
        return flask.redirect("/create-post")
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
    return flask.render_template("profile.html", pages=pages, user=user)


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
        post = database.create_post(user.username, form.text.data)
        return flask.redirect("/profile")
    if form.cancel.data:
        return flask.redirect("/profile")
    return flask.render_template("create_post.html", pages=pages, form=form)