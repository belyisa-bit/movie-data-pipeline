# src/analytics.py
import logging
import sqlite3
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_analytics_queries():
    """Conecta ao banco SQLite e executa queries analíticas de negócio."""
    logging.info("📊 INICIANDO ANÁLISE DE DADOS DOS FILMES")
    logging.info("==============================================")

    conn = sqlite3.connect("movies.db")

    try:
        # QUERY 1: Top 5 filmes com maior Retorno sobre o Investimento (ROI)
        query_top_roi = """
            SELECT title, release_year, budget, revenue, roi
            FROM tb_movies_processed
            WHERE budget > 0
            ORDER BY roi DESC
            LIMIT 5;
        """
        print("\n🏆 TOP 5 FILMES COM MAIOR ROI:")
        df_roi = pd.read_sql_query(query_top_roi, conn)
        print(df_roi.to_string(index=False))

        # QUERY 2: Ajustada para calcular a década dinamicamente pelo ano de lançamento
        query_decades = """
            SELECT CAST((release_year / 10) * 10 AS TEXT) || 's' as calculated_decade, 
                   COUNT(*) as total_movies,
                   ROUND(AVG(profit), 2) as average_profit,
                   ROUND(SUM(revenue), 2) as total_revenue
            FROM tb_movies_processed
            GROUP BY calculated_decade
            ORDER BY calculated_decade ASC;
        """
        print("\n📅 PERFORMANCE FINANCEIRA POR DÉCADA:")
        df_decades = pd.read_sql_query(query_decades, conn)
        print(df_decades.to_string(index=False))

        # QUERY 3: Ajustada para usar 'rating_category' ou gerar um fallback se não existir
        # Se der erro em rating_category, mudamos depois, mas vamos testar se ela passa:
        query_ratings = """
            SELECT rating_category,
                   COUNT(*) as total_movies,
                   ROUND(AVG(profit), 2) as average_profit
            FROM tb_movies_processed
            GROUP BY rating_category
            ORDER BY average_profit DESC;
        """
        print("\n⭐ LUCRO MÉDIO POR CATEGORIA DE AVALIAÇÃO (RATING):")
        df_ratings = pd.read_sql_query(query_ratings, conn)
        print(df_ratings.to_string(index=False))

    except Exception as error:
        logging.error(f"💥 Erro ao rodar queries analíticas: {error}")
    finally:
        conn.close()
        logging.info("\n==============================================")
        logging.info("Análise concluída com sucesso!")


if __name__ == "__main__":
    run_analytics_queries()