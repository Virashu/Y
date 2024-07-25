"""
This type stub file was generated by pyright.
"""

from typing import Any, Callable, Sequence

from flask.sessions import SessionMixin
from markupsafe import Markup
from werkzeug.datastructures import CombinedMultiDict, ImmutableMultiDict, MultiDict
from werkzeug.utils import cached_property
from wtforms import Form
from wtforms.form import BaseForm
from wtforms.meta import DefaultMeta

from .csrf import _FlaskFormCSRF  # type: ignore

SUBMIT_METHODS: set[str] = ...
_Auto: object = ...

class FlaskForm(Form):
    """Flask-specific subclass of WTForms :class:`~wtforms.form.Form`.

    If ``formdata`` is not specified, this will use :attr:`flask.request.form`
    and :attr:`flask.request.files`.  Explicitly pass ``formdata=None`` to
    prevent this.
    """

    class Meta(DefaultMeta):
        csrf_class = _FlaskFormCSRF
        csrf_context: SessionMixin = ...
        @cached_property
        def csrf(self) -> bool: ...  # type: ignore
        @cached_property
        def csrf_secret(self) -> str: ...  # type: ignore
        @cached_property
        def csrf_field_name(self) -> str: ...  # type: ignore
        @cached_property
        def csrf_time_limit(self) -> int: ...  # type: ignore
        def wrap_formdata(
            self, form: BaseForm, formdata: MultiDict[Any, Any] | None
        ) -> (
            CombinedMultiDict[Any, Any]
            | ImmutableMultiDict[str, str]
            | ImmutableMultiDict[Any, Any]
            | None
        ): ...

    def __init__(self, formdata=..., **kwargs: Any) -> None: ...
    def is_submitted(self) -> bool:
        """Consider the form submitted if there is an active request and
        the method is ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        """
        ...

    def validate_on_submit(
        self, extra_validators: dict[str, Sequence[Callable[..., bool]]] = ...
    ) -> bool:
        """Call :meth:`validate` only if the form is submitted.
        This is a shortcut for ``form.is_submitted() and form.validate()``.
        """
        ...

    def hidden_tag(self, *fields: str) -> Markup:
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """
        ...
