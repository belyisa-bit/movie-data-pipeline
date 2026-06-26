from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("data/raw/movies.csv")


def extract_movies() -> pd.DataFrame:
    """
    Extrai os dados do arquivo CSV.
    """

    try:
        df = pd.read_csv(RAW_DATA_PATH)

        print(f"{len(df)} registros carregados com sucesso.")

        return df

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Arquivo não encontrado: {RAW_DATA_PATH}"
        )

    except Exception as error:
        raise RuntimeError(
            f"Erro durante a extração dos dados: {error}"
        )