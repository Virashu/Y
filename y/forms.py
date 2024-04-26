import hashlib

import flask_wtf
import wtforms
from wtforms.validators import DataRequired


def hash(string: str) -> str:
    if not string:
        return string
    return hashlib.md5(string.encode()).hexdigest()


class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField("Username", validators=[DataRequired()])
    password = wtforms.PasswordField(
        "Password", validators=[DataRequired()], filters=[hash]
    )
    remember_me = wtforms.BooleanField("Remember me")
    submit = wtforms.SubmitField("Log in")


class SignupForm(flask_wtf.FlaskForm):
    username = wtforms.StringField("Username", validators=[DataRequired()])
    email = wtforms.StringField("Email", validators=[DataRequired()])
    display_name = wtforms.StringField("Display name", validators=[DataRequired()])
    password = wtforms.PasswordField(
        "Password", validators=[DataRequired()], filters=[hash]
    )
    remember_me = wtforms.BooleanField("Remember me")
    submit = wtforms.SubmitField("Sign up")


class CreatePostForm(flask_wtf.FlaskForm):
    text = wtforms.StringField(validators=[DataRequired()])
    submit = wtforms.SubmitField("Save")
    cancel = wtforms.SubmitField("Cancel")


class EditProfileForm(flask_wtf.FlaskForm):
    username = wtforms.StringField("Username", validators=[DataRequired()])
    email = wtforms.StringField("Email", validators=[DataRequired()])
    password = wtforms.PasswordField(
        "Password", validators=[DataRequired()], filters=[hash]
    )
    display_name = wtforms.StringField("Display name", validators=[DataRequired()])
    description = wtforms.StringField("Description", validators=[DataRequired()])
    submit = wtforms.SubmitField("Save")
    cancel = wtforms.SubmitField("Cancel")
