import flask_wtf
import wtforms

from .form_fields import RequiredPasswordField, RequiredStringField
from .utils import hash_string


class LoginForm(flask_wtf.FlaskForm):
    username = RequiredStringField("Username")
    password = RequiredPasswordField("Password", filters=[hash_string])
    remember_me = wtforms.BooleanField("Remember me")
    submit = wtforms.SubmitField("Log in")


class SignupForm(flask_wtf.FlaskForm):
    username = RequiredStringField("Username")
    email = RequiredStringField("Email")
    display_name = RequiredStringField("Display name")
    password = RequiredPasswordField("Password", filters=[hash_string])
    remember_me = wtforms.BooleanField("Remember me")
    submit = wtforms.SubmitField("Sign up")


class CreatePostForm(flask_wtf.FlaskForm):
    text = RequiredStringField()
    submit = wtforms.SubmitField("Save")
    cancel = wtforms.SubmitField("Cancel")


class EditProfileForm(flask_wtf.FlaskForm):
    username = RequiredStringField("Username")
    email = RequiredStringField("Email")
    password = RequiredPasswordField("Password", filters=[hash_string])
    display_name = RequiredStringField("Display name")
    description = RequiredStringField("Description")
    submit = wtforms.SubmitField("Save")
    cancel = wtforms.SubmitField("Cancel")
