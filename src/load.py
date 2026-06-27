# src/load.py
import logging
import pandas as pd
from sqlalchemy import create_engine
from src.config import Config

logger = logging.getLogger(__name__)


def get_db_connection():
    """Cria o motor de conexão (engine) temporário com SQLite."""
    # COMENTADO TEMPORARIAMENTE (POSTGRESQL):
    # connection_url = f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_DATABASE}"

    # RECURSO TEMPORÁRIO (SQLITE):
    # Isso vai criar um arquivo chamado 'movies.db' na raiz do seu projeto
    connection_url = "sqlite:///movies.db"

    engine = create_engine(connection_url)
    return engine


def load_movies(df: pd.DataFrame, table_name: str = "movies") -> None:
    """Insere o DataFrame processado na tabela do banco SQLite."""
    logging.info(
        f"Iniciando a carga de {df.shape[0]} registros no banco SQLite..."
    )

    try:
        engine = get_db_connection()

        # O Pandas funciona exatamente igual para ambos os bancos!
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
        )

        logging.info(
            f"📥 Sucesso! Dados carregados na tabela '{table_name}' do SQLite."
        )

    except Exception as error:
        logging.error(f"💥 Erro ao carregar dados no SQLite: {error}")
        raise error