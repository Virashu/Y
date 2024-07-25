"""
This type stub file was generated by pyright.
"""

from _typeshed import SupportsItems
from collections.abc import Collection, Iterator, MutableMapping
from typing import Any, Literal, Protocol, TypeVar, overload
from typing_extensions import TypeAlias
from markupsafe import Markup
from wtforms.fields.core import Field, UnboundField
from wtforms.form import BaseForm

_FieldT = TypeVar("_FieldT", bound=Field)

class _SupportsGettextAndNgettext(Protocol):
    def gettext(self, string: str, /) -> str: ...
    def ngettext(self, singular: str, plural: str, n: int, /) -> str: ...

class _MultiDictLikeBase(Protocol):
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __contains__(self, key: Any, /) -> bool: ...

class _MultiDictLikeWithGetlist(_MultiDictLikeBase, Protocol):
    def getlist(self, key: str, /) -> list[Any]: ...

class _MultiDictLikeWithGetall(_MultiDictLikeBase, Protocol):
    def getall(self, key: str, /) -> list[Any]: ...

_MultiDictLike: TypeAlias = ...

class DefaultMeta:
    def bind_field(
        self,
        form: BaseForm,
        unbound_field: UnboundField[_FieldT],
        options: MutableMapping[str, Any],
    ) -> _FieldT: ...
    @overload
    def wrap_formdata(self, form: BaseForm, formdata: None) -> None: ...
    @overload
    def wrap_formdata(
        self, form: BaseForm, formdata: _MultiDictLike
    ) -> _MultiDictLikeWithGetlist: ...
    def render_field(
        self, field: Field, render_kw: SupportsItems[str, Any]
    ) -> Markup: ...

    csrf: bool
    csrf_field_name: str
    csrf_secret: Any | None
    csrf_context: Any | None
    csrf_class: type[Any] | None
    def build_csrf(self, form: BaseForm) -> Any: ...

    locales: Literal[False] | Collection[str]
    cache_translations: bool
    translations_cache: dict[str, _SupportsGettextAndNgettext]
    def get_translations(self, form: BaseForm) -> _SupportsGettextAndNgettext: ...
    def update_values(self, values: SupportsItems[str, Any]) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
