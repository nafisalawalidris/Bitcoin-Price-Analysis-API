import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_username: str = os.getenv("DB_USER", "postgres")
    database_password: str = os.getenv("DB_PASSWORD", "Feenah413")
    database_hostname: str = os.getenv("DB_HOST", "localhost")
    database_port: int = int(os.getenv("DB_PORT", "5432"))
    database_name: str = os.getenv("DB_NAME", "Bitcoin_Prices_Database")
    
    test_database_name: str = "Bitcoin_Prices_Database_test"

    class Config:
        env_file = ".env"

settings = Settings()
