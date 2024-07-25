"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable, Sequence
from decimal import Decimal
from typing import Any, Literal, overload
from typing_extensions import Self
from wtforms.fields.core import Field, _Filter, _FormT, _Validator, _Widget
from wtforms.form import BaseForm
from wtforms.meta import DefaultMeta, _SupportsGettextAndNgettext
from wtforms.utils import UnsetValue

__all__ = (
    "IntegerField",
    "DecimalField",
    "FloatField",
    "IntegerRangeField",
    "DecimalRangeField",
)

class LocaleAwareNumberField(Field):
    use_locale: bool
    number_format: Any | None
    locale: str
    def __init__(
        self,
        label: str | None = ...,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = ...,
        use_locale: bool = ...,
        number_format: str | Any | None = ...,
        *,
        filters: Sequence[_Filter] = ...,
        description: str = ...,
        id: str | None = ...,
        default: object | None = ...,
        widget: _Widget[Self] | None = ...,
        render_kw: dict[str, Any] | None = ...,
        name: str | None = ...,
        _form: BaseForm | None = ...,
        _prefix: str = ...,
        _translations: _SupportsGettextAndNgettext | None = ...,
        _meta: DefaultMeta | None = ...
    ) -> None: ...

class IntegerField(Field):
    data: int | None
    default: int | Callable[[], int] | None
    def __init__(
        self,
        label: str | None = ...,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = ...,
        *,
        filters: Sequence[_Filter] = ...,
        description: str = ...,
        id: str | None = ...,
        default: int | Callable[[], int] | None = ...,
        widget: _Widget[Self] | None = ...,
        render_kw: dict[str, Any] | None = ...,
        name: str | None = ...,
        _form: BaseForm | None = ...,
        _prefix: str = ...,
        _translations: _SupportsGettextAndNgettext | None = ...,
        _meta: DefaultMeta | None = ...
    ) -> None: ...

class DecimalField(LocaleAwareNumberField):
    data: Decimal | None
    default: Decimal | Callable[[], Decimal] | None
    places: int | None
    rounding: str | None
    @overload
    def __init__(
        self,
        label: str | None = ...,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = ...,
        *,
        places: UnsetValue = ...,
        rounding: None = ...,
        use_locale: Literal[True],
        number_format: str | Any | None = ...,
        filters: Sequence[_Filter] = ...,
        description: str = ...,
        id: str | None = ...,
        default: Decimal | Callable[[], Decimal] | None = ...,
        widget: _Widget[Self] | None = ...,
        render_kw: dict[str, Any] | None = ...,
        name: str | None = ...,
        _form: BaseForm | None = ...,
        _prefix: str = ...,
        _translations: _SupportsGettextAndNgettext | None = ...,
        _meta: DefaultMeta | None = ...
    ) -> None: ...
    @overload
    def __init__(
        self,
        label: str | None = ...,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = ...,
        places: int | UnsetValue | None = ...,
        rounding: str | None = ...,
        *,
        use_locale: Literal[False] = ...,
        number_format: str | Any | None = ...,
        filters: Sequence[_Filter] = ...,
        description: str = ...,
        id: str | None = ...,
        default: Decimal | Callable[[], Decimal] | None = ...,
        widget: _Widget[Self] | None = ...,
        render_kw: dict[str, Any] | None = ...,
        name: str | None = ...,
        _form: BaseForm | None = ...,
        _prefix: str = ...,
        _translations: _SupportsGettextAndNgettext | None = ...,
        _meta: DefaultMeta | None = ...
    ) -> None: ...

class FloatField(Field):
    data: float | None
    default: float | Callable[[], float] | None
    def __init__(
        self,
        label: str | None = ...,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = ...,
        *,
        filters: Sequence[_Filter] = ...,
        description: str = ...,
        id: str | None = ...,
        default: float | Callable[[], float] | None = ...,
        widget: _Widget[Self] | None = ...,
        render_kw: dict[str, Any] | None = ...,
        name: str | None = ...,
        _form: BaseForm | None = ...,
        _prefix: str = ...,
        _translations: _SupportsGettextAndNgettext | None = ...,
        _meta: DefaultMeta | None = ...
    ) -> None: ...

class IntegerRangeField(IntegerField): ...
class DecimalRangeField(DecimalField): ...
