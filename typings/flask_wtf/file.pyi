from typing import Any, Iterable, TypeAlias, override

from _typeshed import Incomplete

__all__ = (
    "FileField",
    "MultipleFileField",
    "FileRequired",
    "FileAllowed",
    "FileSize",
    "file_required",
    "file_allowed",
    "file_size",
)

from werkzeug.datastructures import FileStorage
from wtforms import Field
from wtforms import FileField as _FileField
from wtforms import MultipleFileField as _MultipleFileField
from wtforms.form import BaseForm
from wtforms.validators import DataRequired

class FileField(_FileField):
    """Werkzeug-aware subclass of :class:`wtforms.fields.FileField`."""

    @override
    def process_formdata(self, valuelist: Iterable[FileStorage | Any]) -> None: ...

class MultipleFileField(_MultipleFileField):
    """Werkzeug-aware subclass of :class:`wtforms.fields.MultipleFileField`.

    .. versionadded:: 1.2.0
    """

    @override
    def process_formdata(self, valuelist: Iterable[FileStorage | Any]) -> None: ...

class FileRequired(DataRequired):
    """Validates that the uploaded files(s) is a Werkzeug
    :class:`~werkzeug.datastructures.FileStorage` object.

    :param message: error message

    You can also use the synonym ``file_required``.
    """

    @override
    def __call__(self, form: BaseForm, field: Field) -> None: ...

file_required: TypeAlias = FileRequired

class FileAllowed:
    """Validates that the uploaded file(s) is allowed by a given list of
    extensions or a Flask-Uploads :class:`~flaskext.uploads.UploadSet`.

    :param upload_set: A list of extensions or an
        :class:`~flaskext.uploads.UploadSet`
    :param message: error message

    You can also use the synonym ``file_allowed``.
    """

    def __init__(
        self, upload_set: Iterable[Incomplete] | Incomplete, message: str | None = None
    ) -> None: ...
    def __call__(self, form: BaseForm, field: Field) -> None: ...

file_allowed: TypeAlias = FileAllowed

class FileSize:
    """Validates that the uploaded file(s) is within a minimum and maximum
    file size (set in bytes).

    :param min_size: minimum allowed file size (in bytes). Defaults to 0 bytes.
    :param max_size: maximum allowed file size (in bytes).
    :param message: error message

    You can also use the synonym ``file_size``.
    """

    def __init__(
        self, max_size: int, min_size: int = 0, message: str | None = None
    ) -> None: ...
    def __call__(self, form: BaseForm, field: Field) -> None: ...

file_size: TypeAlias = FileSize
