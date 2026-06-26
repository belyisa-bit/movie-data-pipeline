from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    """
    Cria e retorna uma conexão com SQLite.
    """

    engine = create_engine(
        "sqlite:///movies.db",
        echo=False
    )

    return engine