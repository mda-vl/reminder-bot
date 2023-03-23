from sqlalchemy import create_engine, Engine

from utils import states


def get_engine() -> Engine:
    path = states.config.db_dir / "file.db"
    # print(type(path))
    return create_engine(f"sqlite:///{path}", echo=True)
