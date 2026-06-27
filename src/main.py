# src/main.py
import logging
import os
from src.config import Config
from src.extract import extract_movies
from src.transform import transform_movies
from src.load import load_movies  # 🚀 NOVO: Importa a camada de carga

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline() -> None:
    logging.info("==============================================")
    logging.info("🎬 INICIANDO O MOVIE DATA PIPELINE (ETL)")
    logging.info("==============================================")

    try:
        # 1. ETAPA: EXTRACT
        df_raw = extract_movies()

        # 2. ETAPA: TRANSFORM
        df_processed = transform_movies(df_raw)

        # 3. ETAPA: EXPORT (CSV intermediário)
        output_path = Config.PROCESSED_DATA_PATH
        logging.info(f"Exportando dados intermediários para: {output_path}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_processed.to_csv(output_path, index=False)

        # 4. ETAPA: LOAD 🚀 (NOVO)
        # O pipeline agora envia os dados direto para o PostgreSQL local
        load_movies(df_processed, table_name="tb_movies_processed")

        logging.info("==============================================")
        logging.info("🏆 PIPELINE EXECUTADO DE PONTA A PONTA COM SUCESSO!")
        logging.info("==============================================")

    except Exception as error:
        logging.critical(f"💥 O pipeline falhou: {error}")


if __name__ == "__main__":
    run_pipeline()