from typing import Any, Callable, Self, Sequence
from wtforms import PasswordField, StringField
from wtforms.form import BaseForm
from wtforms.meta import DefaultMeta
from wtforms.validators import DataRequired
from _typeshed import Incomplete


class RequiredStringField(StringField):
    """
    Data is guaranteed to be not None.
    """

    data: str  # type: ignore

    def __init__(
        self,
        label: str | None = None,
        validators: tuple[Incomplete[Incomplete, Self], ...] | list[Any] | None = None,
        filters: Sequence[Incomplete] = (),
        description: str = "",
        id: str | None = None,
        default: str | Callable[[], str] | None = None,
        widget: Incomplete[Self] | None = None,
        render_kw: dict[str, Any] | None = None,
        name: str | None = None,
        _form: BaseForm | None = None,
        _prefix: str = "",
        _translations: Incomplete | None = None,
        _meta: DefaultMeta | None = None,
    ) -> None:
        validators = list(validators or [])
        validators.insert(0, DataRequired())
        super().__init__(
            label,
            validators,
            filters,
            description,
            id,
            default,
            widget,
            render_kw,
            name,
            _form,
            _prefix,
            _translations,
            _meta,
        )


class RequiredPasswordField(RequiredStringField, PasswordField):

    data: str  # type: ignore
