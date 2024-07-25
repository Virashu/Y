import pathlib

import flask
import flask_login
import werkzeug

from flask.typing import ResponseReturnValue

from .database import database
from .database.database import db_session
from .database.post import Post
from .database.user import User
from .forms import CreatePostForm, EditProfileForm, LoginForm, SignupForm
from .utils import hash_string, make_salt

ROOT = str(pathlib.Path(__file__).parent.parent.resolve())  # Path of the project

app = flask.Flask(
    __name__,
    template_folder=f"{ROOT}/templates",
    static_folder=f"{ROOT}/static",
    static_url_path="/static",
)

app.config["SECRET_KEY"] = "huh"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@login_manager.unauthorized_handler  # type: ignore
def unauthorized() -> werkzeug.Response:
    return flask.redirect("/login")


@app.route("/", methods=["GET", "POST"])
def index() -> ResponseReturnValue:
    user: User = flask_login.current_user  # type: ignore

    if flask.request.method == "POST":
        reaction = flask.request.form.get("reaction")

        if reaction:
            if not user.is_authenticated:
                return unauthorized()

            database.reaction_to_post(reaction, str(user.username))

    posts = database.get_all_posts()
    return flask.render_template("index.html", user=user, posts=posts)


@app.route("/signup", methods=["GET", "POST"])
def signup() -> ResponseReturnValue:
    form: SignupForm = SignupForm()

    if form.submit.data and form.validate_on_submit():
        # salted
        salt = make_salt()
        password_str = hash_string(salt + form.password.data)

        user = database.create_user(
            form.username.data,
            form.display_name.data,
            form.email.data,
            password_str,
            salt,
        )

        if user:
            if flask_login.login_user(user, remember=form.remember_me.data):
                return flask.redirect("/")

        return flask.render_template(
            "signup.html",
            message="Error",
            form=form,
            is_logged_in=False,
        )

    return flask.render_template("signup.html", form=form, is_logged_in=False)


@app.route("/login", methods=["GET", "POST"])
def login() -> ResponseReturnValue:
    user: User = flask_login.current_user  # type: ignore

    if user:
        flask_login.logout_user()

    form: LoginForm = LoginForm()

    if form.submit.data and form.validate_on_submit():
        user: User | None = database.login_user(form.username.data, form.password.data)

        if user:
            flask_login.login_user(user, remember=form.remember_me.data)
            return flask.redirect("/")

        return flask.render_template(
            "login.html", message="Wrong username or password", form=form, user=user
        )

    return flask.render_template("login.html", form=form, user=None)


@app.route("/profile", methods=["GET", "POST"])
def profile() -> ResponseReturnValue:
    if flask.request.method == "POST":
        if post_id := flask.request.form.get("reaction", None):
            user: User = flask_login.current_user  # type: ignore

            if not user.is_authenticated:
                return unauthorized()

            database.reaction_to_post(post_id, str(user.username))

        elif post_id := flask.request.form.get("delete"):
            database.delete_post(post_id)
            return flask.redirect("/profile")

    username = flask.request.args.get("u", None)

    if username:
        user = database.get_user_by_username(username)
        if not user:
            return flask.render_template("error.html", message="User Not Found")
    else:
        user = flask_login.current_user  # type: ignore
        if not user.is_authenticated:
            return unauthorized()

    posts = database.get_posts_by_user(user.username)  # type: ignore

    return flask.render_template("profile.html", user=user, posts=posts)


@app.route("/delete-post", methods=["POST"])
@flask_login.login_required
def delete_post() -> ResponseReturnValue:
    post_id = flask.request.form.get("delete")

    if not post_id:
        return flask.redirect("/profile")

    user: User = flask_login.current_user  # type: ignore
    post = database.get_post_by_id(post_id)

    if not post:
        return flask.render_template("error.html", message="Post Not Found")

    if str(user.username) == str(post.author):
        database.delete_post(post_id)

    return flask.redirect("/profile")


@app.route("/create-post", methods=["GET", "POST"])
@flask_login.login_required
def create_post() -> ResponseReturnValue:
    form = CreatePostForm()

    if form.submit.data:
        user: User = flask_login.current_user  # type: ignore

        username = str(user.username)

        answer_to = flask.request.args.get("answer_to")

        back = flask.request.values["back"]
        post = database.create_post(username, form.text.data, answer_to)

        if not post:
            return flask.render_template("error.html", message="Error creating post")

        return flask.redirect(f"/post?post_id={post.id}&back={back}")

    if form.cancel.data:
        answer_to = flask.request.values.get("answer_to")

        if answer_to:
            back = flask.request.values["back"]
            return flask.redirect(f"/post?post_id={answer_to}&back={back}")

        return flask.redirect("/profile")

    return flask.render_template("create_post.html", form=form)


@app.route("/edit-post", methods=["GET", "POST"])
@flask_login.login_required
def edit_post() -> ResponseReturnValue:
    form = CreatePostForm()

    post_id = flask.request.args.get("post_id")

    if not post_id:
        return flask.render_template("error.html", message="Post Not Found")

    if form.submit.data:
        text = form.text.data

        database.edit_post(post_id, text)
        return flask.redirect("/profile")

    if form.cancel.data:
        return flask.redirect("/profile")

    post = database.get_post_by_id(post_id)

    if not post:
        return flask.render_template("error.html", message="Post Not Found")

    user: User = flask_login.current_user  # type: ignore

    if str(post.author) != str(user.username):
        return flask.render_template("error.html", message="Post Not Found")

    form.text.data = post.text
    return flask.render_template("create_post.html", form=form)


@app.route("/edit-profile", methods=["GET", "POST"])
@flask_login.login_required
def edit_profile() -> ResponseReturnValue:
    form = EditProfileForm()

    user: User = flask_login.current_user  # type: ignore

    if form.submit.data:
        database.edit_user(
            form.username.data,
            form.display_name.data,
            form.description.data,
            form.email.data,
            form.password.data,
        )
        return flask.redirect("/profile")
    if form.cancel.data:
        return flask.redirect("/profile")

    form.username.data = str(user.username)
    form.email.data = str(user.email)
    form.display_name.data = str(user.display_name)
    form.description.data = str(user.description)

    return flask.render_template("edit_profile.html", form=form)


@app.route("/post", methods=["GET", "POST"])
def post_details() -> ResponseReturnValue:
    """Detailed post info"""

    if flask.request.method == "POST":
        if "answer" in flask.request.form:
            return flask.redirect(
                "/create-post"
                + f"?answer_to={flask.request.values['post_id']}"
                + f"&back={flask.request.values['back']}"
            )

        if reaction := flask.request.form.get("reaction"):
            user: User = flask_login.current_user  # type: ignore

            if not user.is_authenticated:
                return unauthorized()

            database.reaction_to_post(reaction, str(user.username))

        else:
            return flask.redirect(f"/{flask.request.values['back']}")

    user = flask_login.current_user  # type: ignore

    post_id = flask.request.values["post_id"]

    post: Post | None = database.get_post_by_id(post_id)
    comments = database.get_answers_to_post(post_id)

    comments.sort(key=lambda x: int(str(x.reactions)), reverse=True)

    return flask.render_template(
        "post_with_comments.html", user=user, post=post, comments=comments
    )
