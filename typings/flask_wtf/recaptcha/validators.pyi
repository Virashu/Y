from typing import Literal

from wtforms import Field
from wtforms.form import BaseForm

RECAPTCHA_VERIFY_SERVER_DEFAULT = ...
RECAPTCHA_ERROR_CODES = ...
__all__ = ["Recaptcha"]

class Recaptcha:
    """Validates a ReCaptcha."""

    def __init__(self, message: str = ...) -> None: ...
    def __call__(self, form: BaseForm, field: Field) -> Literal[True] | None: ...
