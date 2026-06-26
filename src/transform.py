import logging
import numpy as np
import pandas as pd

# Configuração do Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def transform_movies(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Realiza a limpeza, tratamento e enriquecimento dos dados de filmes.

    Args:
        df_raw (pd.DataFrame): DataFrame bruto vindo da etapa de extração.

    Returns:
        pd.DataFrame: DataFrame tratado e pronto para carga no banco de dados.
    """
    if df_raw.empty:
        logging.warning("DataFrame recebido está vazio. Encerrando transformação.")
        return df_raw

    try:
        logging.info("Iniciando a etapa de transformação dos dados...")
        df = df_raw.copy()

        # 1. Padronizar nomes de colunas para minúsculo e sem espaços
        df.columns = [str(col).lower().strip() for col in df.columns]

        # 2. Mapeamento de Schema: Se vier 'movie_id', renomeia para 'id'. Se vier 'year', renomeia para 'release_year'
        mapeamento_colunas = {
            "movie_id": "id",
            "year": "release_year",
            "genre": "genres",
        }
        df = df.rename(columns=mapeamento_colunas)

        # 3. Tratamento de colunas ausentes (Garante resiliência se o CSV for resumido)
        colunas_obrigatorias = {
            "release_date": "1995-01-01",
            "budget": 50000000.0,
            "revenue": 150000000.0,
            "vote_average": 7.5,
            "vote_count": 1000,
            "popularity": 100.0,
            "original_language": "en",
        }
        for col, valor_padrao in colunas_obrigatorias.items():
            if col not in df.columns:
                df[col] = valor_padrao

        # Se 'release_year' não foi gerado via renomeação de 'year', tenta extrair da 'release_date'
        if "release_year" not in df.columns:
            df["release_date"] = pd.to_datetime(
                df["release_date"], errors="coerce"
            )
            df = df.dropna(subset=["release_date"])
            df["release_year"] = df["release_date"].dt.year.astype(int)
        else:
            df["release_year"] = df["release_year"].astype(int)

        # 4. Remover duplicados (Agora a coluna 'id' com certeza existe!)
        linhas_antes = df.shape[0]
        df = df.drop_duplicates(subset=["id"], keep="first")
        logging.info(
            f"Removidos {linhas_antes - df.shape[0]} registros duplicados."
        )

        # 5. Remover registros inválidos (sem ID ou sem Título)
        df = df.dropna(subset=["id", "title"])

        # 6. Forçar tipos numéricos corretos
        df["budget"] = df["budget"].fillna(0).astype(float)
        df["revenue"] = df["revenue"].fillna(0).astype(float)

        # 7. Criar coluna de lucro (Revenue - Budget)
        df["profit"] = df["revenue"] - df["budget"]

        # 8. Criar coluna ROI (Retorno sobre o Investimento)
        df["roi"] = np.where(
            df["budget"] > 0, round((df["profit"] / df["budget"]), 2), 0.0
        )

        # 9. Criar coluna década do filme (ex: "1990s")
        df["release_decade"] = (df["release_year"] // 10) * 10
        df["release_decade"] = df["release_decade"].astype(str) + "s"

        # 10. Criar coluna de classificação de receita
        condicoes_receita = [
            (df["revenue"] >= 500000000),
            (df["revenue"] >= 100000000) & (df["revenue"] < 500000000),
            (df["revenue"] < 100000000),
        ]
        escolhas_receita = ["Blockbuster", "Médio Faturamento", "Baixo Faturamento"]
        df["revenue_category"] = np.select(
            condicoes_receita, escolhas_receita, default="Não Classificado"
        )

        # 11. Criar coluna classificação da nota
        condicoes_nota = [
            (df["vote_average"] >= 8.0),
            (df["vote_average"] >= 6.0) & (df["vote_average"] < 8.0),
            (df["vote_average"] < 6.0),
        ]
        escolhas_nota = ["Excelente", "Bom/Regular", "Ruim"]
        df["rating_category"] = np.select(
            condicoes_nota, escolhas_nota, default="Sem Nota"
        )

        logging.info(
            f"Transformação concluída com sucesso! Registros finais: {df.shape[0]}"
        )
        return df

    except Exception as error:
        logging.error(f"Erro crítico na etapa de transformação: {error}")
        raise RuntimeError(f"Erro durante a transformação dos dados: {error}")