# src/main.py
import logging
import os
from src.config import Config  # Importando a classe limpa e validada
from src.extract import extract_movies
from src.transform import transform_movies

# Configuração do Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_pipeline() -> None:
    """Executa o fluxo principal do pipeline ETL até a exportação dos dados."""
    logging.info("==============================================")
    logging.info("🎬 INICIANDO O MOVIE DATA PIPELINE (ETL)")
    logging.info("==============================================")

    try:
        # 1. ETAPA: EXTRACT
        df_raw = extract_movies()

        # 2. ETAPA: TRANSFORM
        df_processed = transform_movies(df_raw)

        # 3. ETAPA: EXPORT
        output_path = Config.PROCESSED_DATA_PATH
        logging.info(f"Exportando dados processados para: {output_path}")

        # Garante que a pasta 'data/processed' existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Salva o DataFrame tratado em um arquivo CSV
        df_processed.to_csv(output_path, index=False)
        logging.info(
            f"🚀 Sucesso! Arquivo gerado com {df_processed.shape[0]} linhas."
        )

    except Exception as error:
        logging.critical(f"💥 O pipeline falhou: {error}")

if __name__ == "__main__":
    run_pipeline()