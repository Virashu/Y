__all__ = ("global_init", "create_session", "SqlAlchemyBase")

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Missing file argument")

    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    if __factory is None:
        raise RuntimeError("Call global_init() first")
    return __factory()
