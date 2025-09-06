from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn, SecretStr

class Settings(BaseSettings):
    """
    Manages application settings and environment variables.
    """
    # Uvicorn server settings
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    
    # Database connection URL
    DATABASE_URL: PostgresDsn
    
    # Redis connection URL
    REDIS_URL: RedisDsn
    
    # API keys and secrets
    OPENAI_API_KEY: SecretStr
    REDDIT_CLIENT_ID: SecretStr
    REDDIT_CLIENT_SECRET: SecretStr
    REDDIT_USER_AGENT: str


    # Pydantic-settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",          # Load settings from a .env file
        env_file_encoding="utf-8",
        extra="ignore"            # Ignore extra fields from the .env file
    )

# Create a single, importable instance of the settings
settings = Settings()