__all__ = ("SqlAlchemyBase", "SessionFactory")

import sqlalchemy as sa
from sqlalchemy import orm

SqlAlchemyBase = orm.declarative_base()


# pylint: disable=too-few-public-methods
class SessionFactory:
    # pylint: disable=unsubscriptable-object  # (sessionmaker is Generic)
    _factory: orm.sessionmaker[orm.Session] | None = None

    def __init__(self, db_file: str) -> None:
        db_url = f"sqlite:///{db_file.strip()}?check_same_thread=False"

        engine = sa.create_engine(db_url, echo=False)
        self._factory = orm.sessionmaker(engine)

        SqlAlchemyBase.metadata.create_all(engine)

    def create_session(self) -> orm.Session:
        if self._factory is None:
            raise RuntimeError("DB is not initialized")

        return self._factory()
