import datetime
from types import NotImplementedType
from typing import Any, Callable, Literal, TypeAlias, TypeVar

from _typeshed import Incomplete
from blinker import NamedSignal
from flask import Flask, Request, Response
from flask.testing import FlaskClient
from typing_extensions import deprecated

__version__: str
__all__ = [
    "__version__",
    "AUTH_HEADER_NAME",
    "COOKIE_DURATION",
    "COOKIE_HTTPONLY",
    "COOKIE_NAME",
    "COOKIE_SECURE",
    "ID_ATTRIBUTE",
    "LOGIN_MESSAGE",
    "LOGIN_MESSAGE_CATEGORY",
    "REFRESH_MESSAGE",
    "REFRESH_MESSAGE_CATEGORY",
    "LoginManager",
    "AnonymousUserMixin",
    "UserMixin",
    "session_protected",
    "user_accessed",
    "user_loaded_from_cookie",
    "user_loaded_from_request",
    "user_logged_in",
    "user_logged_out",
    "user_login_confirmed",
    "user_needs_refresh",
    "user_unauthorized",
    "FlaskLoginClient",
    "confirm_login",
    "current_user",
    "decode_cookie",
    "encode_cookie",
    "fresh_login_required",
    "login_fresh",
    "login_remembered",
    "login_required",
    "login_url",
    "login_user",
    "logout_user",
    "make_next_param",
    "set_login_view",
]

# config.py

COOKIE_NAME: str
COOKIE_DURATION: datetime.timedelta
COOKIE_SECURE: bool
COOKIE_HTTPONLY: bool
COOKIE_SAMESITE: Incomplete
LOGIN_MESSAGE: str
LOGIN_MESSAGE_CATEGORY: str
REFRESH_MESSAGE: str
REFRESH_MESSAGE_CATEGORY: str
ID_ATTRIBUTE: str
AUTH_HEADER_NAME: str
SESSION_KEYS: set[str]
EXEMPT_METHODS: set[str]
USE_SESSION_FOR_NEXT: bool

# mixins.py

class UserMixin:
    def __hash__(self: object) -> int: ...
    @property
    def is_active(self) -> Literal[True]: ...
    @property
    def is_authenticated(self) -> Literal[True]: ...
    @property
    def is_anonymous(self) -> Literal[False]: ...
    def get_id(self) -> str: ...
    def __eq__(self, other: object) -> bool | NotImplementedType: ...
    def __ne__(self, other: object) -> bool | NotImplementedType: ...

class AnonymousUserMixin:
    @property
    def is_authenticated(self) -> Literal[False]: ...
    @property
    def is_active(self) -> Literal[False]: ...
    @property
    def is_anonymous(self) -> Literal[True]: ...
    def get_id(self) -> None: ...

# signals.py

user_logged_in: NamedSignal
user_logged_out: NamedSignal
user_loaded_from_cookie: NamedSignal
user_loaded_from_request: NamedSignal
user_login_confirmed: NamedSignal
user_unauthorized: NamedSignal
user_needs_refresh: NamedSignal
user_accessed: NamedSignal
session_protected: NamedSignal

# utils.py

_Wrapped = TypeVar("_Wrapped", bound=object)

current_user: UserMixin

def encode_cookie(payload: str, key: str | None = None) -> str: ...
def decode_cookie(cookie: str, key: str | None = None) -> str | None: ...
def make_next_param(login_url: str, current_url: str) -> str: ...
def expand_login_view(login_view: str) -> str: ...
def login_url(
    login_view: str, next_url: str | None = None, next_field: str = "next"
) -> str: ...
def login_fresh() -> bool: ...
def login_remembered() -> bool: ...
def login_user(
    user: object,
    remember: bool = False,
    duration: datetime.timedelta | None = None,
    force: bool = False,
    fresh: bool = True,
) -> bool: ...
def logout_user() -> Literal[True]: ...
def confirm_login() -> None: ...
def login_required(func: _Wrapped) -> _Wrapped: ...
def fresh_login_required(func: _Wrapped) -> _Wrapped: ...
def set_login_view(login_view: str, blueprint: object | None = None) -> None: ...

class FlaskLoginClient(FlaskClient):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

UserCallback: TypeAlias = Callable[[str], UserMixin | None]
WrappedUserCallback = TypeVar("WrappedUserCallback", bound=UserCallback)

RequestCallback: TypeAlias = Callable[[Request], UserMixin | None]
WrappedRequestCallback = TypeVar("WrappedRequestCallback", bound=RequestCallback)

UnauthorizedCallback: TypeAlias = Callable[[], Response]
WrappedUnauthorizedCallback = TypeVar(
    "WrappedUnauthorizedCallback", bound=UnauthorizedCallback
)

NeedsRefreshCallback: TypeAlias = Callable[[], Response]
WrappedNeedsRefreshCallback = TypeVar(
    "WrappedNeedsRefreshCallback", bound=NeedsRefreshCallback
)

class LoginManager:
    anonymous_user: AnonymousUserMixin
    login_view: Incomplete
    blueprint_login_views: Incomplete
    login_message: str
    login_message_category: str
    refresh_view: Incomplete
    needs_refresh_message: str
    needs_refresh_message_category: str
    session_protection: str
    localize_callback: Callable[[str], str]
    unauthorized_callback: UnauthorizedCallback
    needs_refresh_callback: NeedsRefreshCallback
    id_attribute: str
    def __init__(
        self, app: Flask | None = None, add_context_processor: bool = True
    ) -> None: ...
    def setup_app(self, app: Flask, add_context_processor: bool = True) -> None: ...
    def init_app(self, app: Flask, add_context_processor: bool = True) -> None: ...
    def unauthorized(self) -> Response: ...
    def user_loader(self, callback: WrappedUserCallback) -> WrappedUserCallback: ...
    @property
    def user_callback(self) -> UserCallback: ...
    def request_loader(
        self, callback: WrappedRequestCallback
    ) -> WrappedRequestCallback: ...
    @property
    def request_callback(self) -> RequestCallback: ...
    def unauthorized_handler(
        self, callback: WrappedUnauthorizedCallback
    ) -> WrappedUnauthorizedCallback: ...
    def needs_refresh_handler(
        self, callback: WrappedNeedsRefreshCallback
    ) -> WrappedNeedsRefreshCallback: ...
    def needs_refresh(self) -> Response: ...
    @deprecated(
        "'header_loader' is deprecated and will be removed in"
        " Flask-Login 0.7. Use 'request_loader' instead."
    )
    def header_loader(self, callback: _Wrapped) -> _Wrapped: ...
