# src/config.py
import os
import logging
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class Config:
    """Classe central de configuração do projeto."""
    
    # Caminhos de dados
    RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", "data/raw/movies.csv")
    PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH", "data/processed/movies_cleaned.csv")
    
    # Credenciais do Banco de Dados
    DB_USER = os.getenv("DB_USER") or os.getenv("user") or os.getenv("USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD") or os.getenv("password") or os.getenv("PASSWORD")
    DB_HOST = os.getenv("DB_HOST") or os.getenv("host") or os.getenv("HOST")
    DB_PORT = os.getenv("DB_PORT") or os.getenv("port") or os.getenv("PORT")
    DB_DATABASE = os.getenv("DB_DATABASE") or os.getenv("database") or os.getenv("DATABASE") or os.getenv("DB_NAME") or os.getenv("db_name")

    @classmethod
    def validate(cls):
        """Valida se todas as credenciais obrigatórias foram carregadas."""
        missing_vars = []
        credenciais = {
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD,
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "database": cls.DB_DATABASE
        }
        
        for nome, valor in credenciais.items():
            if not valor:
                missing_vars.append(nome)
                
        if missing_vars:
            raise ValueError(
                f"As seguintes variáveis de ambiente não foram definidas no .env: {missing_vars}"
            )

# Executa a validação assim que o módulo for importado
Config.validate()