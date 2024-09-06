from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: int
    database_name: str

    # Optional: Additional settings for the API
    test_database_name: str = "Bitcoin_Prices_Database_test"  # Default test database name
    api_key: str = None  # Example: for real-time data integration with exchanges
    debug: bool = False  # Toggle debug mode

    class Config:
        env_file = ".env"  # Path to the environment variables file
        env_prefix = "DB_"  # Prefix for environment variables to match class attributes

# Initialize settings
settings = Settings()
