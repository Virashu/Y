from typing import Any, TypeVar, Union, override
from flask import Blueprint, Flask
from werkzeug.exceptions import BadRequest
from wtforms import Field
from wtforms.csrf.core import CSRF, CSRFTokenField
from wtforms.form import BaseForm

__all__ = ("generate_csrf", "validate_csrf", "CSRFProtect")
logger = ...

def generate_csrf(secret_key: str = ..., token_key: str = ...) -> Any:
    """Generate a CSRF token. The token is cached for a request, so multiple
    calls to this function will generate the same token.

    During testing, it might be useful to access the signed token in
    ``g.csrf_token`` and the raw token in ``session['csrf_token']``.

    :param secret_key: Used to securely sign the token. Default is
        ``WTF_CSRF_SECRET_KEY`` or ``SECRET_KEY``.
    :param token_key: Key where token is stored in session for comparison.
        Default is ``WTF_CSRF_FIELD_NAME`` or ``'csrf_token'``.
    """
    ...

def validate_csrf(
    data: str, secret_key: str = ..., time_limit: int = ..., token_key: str = ...
) -> None:
    """Check if the given data is a valid CSRF token. This compares the given
    signed token to the one stored in the session.

    :param data: The signed CSRF token to be checked.
    :param secret_key: Used to securely sign the token. Default is
        ``WTF_CSRF_SECRET_KEY`` or ``SECRET_KEY``.
    :param time_limit: Number of seconds that the token is valid. Default is
        ``WTF_CSRF_TIME_LIMIT`` or 3600 seconds (60 minutes).
    :param token_key: Key where token is stored in session for comparison.
        Default is ``WTF_CSRF_FIELD_NAME`` or ``'csrf_token'``.

    :raises ValidationError: Contains the reason that validation failed.

    .. versionchanged:: 0.14
        Raises ``ValidationError`` with a specific error message rather than
        returning ``True`` or ``False``.
    """
    ...

class _FlaskFormCSRF(CSRF):
    @override
    def generate_csrf_token(self, csrf_token_field: CSRFTokenField) -> Any: ...
    @override
    def validate_csrf_token(self, form: BaseForm, field: Field) -> None: ...

_T = TypeVar("_T", bound=Union[Blueprint, str, Any])

class CSRFProtect:
    """Enable CSRF protection globally for a Flask app.

    ::

        app = Flask(__name__)
        csrf = CSRFProtect(app)

    Checks the ``csrf_token`` field sent with forms, or the ``X-CSRFToken``
    header sent with JavaScript requests. Render the token in templates using
    ``{{ csrf_token() }}``.

    See the :ref:`csrf` documentation.
    """

    def __init__(self, app: Flask | None = ...) -> None: ...
    def init_app(self, app: Flask) -> None: ...
    def protect(self) -> None: ...
    def exempt(self, view: _T) -> _T:
        """Mark a view or blueprint to be excluded from CSRF protection.

        ::

            @app.route('/some-view', methods=['POST'])
            @csrf.exempt
            def some_view():
                ...

        ::

            bp = Blueprint(...)
            csrf.exempt(bp)

        """
        ...

class CSRFError(BadRequest):
    """Raise if the client sends invalid CSRF data with the request.

    Generates a 400 Bad Request response with the failure reason by default.
    Customize the response by registering a handler with
    :meth:`flask.Flask.errorhandler`.
    """

    description: str

def same_origin(current_uri: str, compare_uri: str) -> bool: ...
