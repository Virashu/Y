import pathlib

ROOT: str = str(pathlib.Path(__file__).parent.parent.resolve())
DB_PATH: str = f"{ROOT}/runtime/y.db"
