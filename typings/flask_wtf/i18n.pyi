__all__ = ("Translations", "translations")

class Translations:
    def gettext(self, string: str) -> str: ...
    def ngettext(self, singular: str, plural: str, n: int) -> str: ...

translations: Translations
