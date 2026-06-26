import os

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
}

missing_vars = [key for key, value in DB_CONFIG.items() if not value]

if missing_vars:
    raise ValueError(
        f"As seguintes variáveis de ambiente não foram definidas: {missing_vars}"
    )