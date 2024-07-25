"""
This type stub file was generated by pyright.
"""

from wtforms import FileField as _FileField, MultipleFileField as _MultipleFileField
from wtforms.validators import DataRequired

class FileField(_FileField):
    """Werkzeug-aware subclass of :class:`wtforms.fields.FileField`."""

    def process_formdata(self, valuelist):  # -> None:
        ...

class MultipleFileField(_MultipleFileField):
    """Werkzeug-aware subclass of :class:`wtforms.fields.MultipleFileField`.

    .. versionadded:: 1.2.0
    """

    def process_formdata(self, valuelist):  # -> None:
        ...

class FileRequired(DataRequired):
    """Validates that the uploaded files(s) is a Werkzeug
    :class:`~werkzeug.datastructures.FileStorage` object.

    :param message: error message

    You can also use the synonym ``file_required``.
    """

    def __call__(self, form, field):  # -> None:
        ...

file_required = FileRequired

class FileAllowed:
    """Validates that the uploaded file(s) is allowed by a given list of
    extensions or a Flask-Uploads :class:`~flaskext.uploads.UploadSet`.

    :param upload_set: A list of extensions or an
        :class:`~flaskext.uploads.UploadSet`
    :param message: error message

    You can also use the synonym ``file_allowed``.
    """

    def __init__(self, upload_set, message=...) -> None: ...
    def __call__(self, form, field):  # -> None:
        ...

file_allowed = FileAllowed

class FileSize:
    """Validates that the uploaded file(s) is within a minimum and maximum
    file size (set in bytes).

    :param min_size: minimum allowed file size (in bytes). Defaults to 0 bytes.
    :param max_size: maximum allowed file size (in bytes).
    :param message: error message

    You can also use the synonym ``file_size``.
    """

    def __init__(self, max_size, min_size=..., message=...) -> None: ...
    def __call__(self, form, field):  # -> None:
        ...

file_size = FileSize
