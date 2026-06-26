# tests/test_transform.py
from src.extract import extract_movies
from src.transform import transform_movies


def test_pipeline_transform():
    print("\n==============================================")
    print("🚀 INICIANDO TESTE DA CAMADA DE TRANSFORMAÇÃO")
    print("==============================================\n")

    # 1. Busca os dados usando o extract
    df_raw = extract_movies()

    # 2. Processa os dados usando o transform
    df_processed = transform_movies(df_raw)

    print("\n--- 📋 Colunas Criadas na Transformação ---")
    print(df_processed.columns.tolist())

    print("\n--- 🎬 Amostra do Resultado Final ---")
    print(
        df_processed[
            [
                "title",
                "profit",
                "roi",
                "release_decade",
                "revenue_category",
                "rating_category",
            ]
        ].head()
    )


if __name__ == "__main__":
    test_pipeline_transform()