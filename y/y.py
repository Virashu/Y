import flask
import pathlib


ROOT = str(pathlib.Path(__file__).parent.parent.resolve())  # Path of the project

app = flask.Flask(__name__, template_folder=f"{ROOT}/templates")


@app.route("/", methods=["GET", "POST"])
def index(): ...


@app.route("/signup", methods=["GET", "POST"])
def signup(): ...


@app.route("/login", methods=["GET", "POST"])
def login(): ...


@app.route("/profile", methods=["GET", "POST"])
def profile(): ...
