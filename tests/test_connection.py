from src.database import get_engine

def test_connection():
    engine = get_engine()

    with engine.connect():
        print("Conexão com SQLite realizada com sucesso!")


if __name__ == "__main__":
    test_connection()