import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn, SecretStr

class Settings(BaseSettings):
    """
    Manages application settings and environment variables.
    """
    # --- Application ---
    ENVIRONMENT: str = "dev"

    # --- Uvicorn Server ---
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000

    # --- Database & Cache ---
    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn

    # --- API Keys ---
    OPENAI_API_KEY: SecretStr
    REDDIT_CLIENT_ID: SecretStr
    REDDIT_CLIENT_SECRET: SecretStr
    REDDIT_USER_AGENT: str

    # --- NEW: Agent Configuration ---
    AGENT_POST_FETCH_LIMIT: int = 20
    AGENT_FILTER_MODEL: str = "gpt-4o-mini"
    AGENT_EXTRACTION_MODEL: str = "gpt-4o"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

class TestSettings(Settings):
    """Settings class specifically for the test environment."""
    # Override agent settings for faster tests
    AGENT_POST_FETCH_LIMIT: int = 5
    
    model_config = SettingsConfigDict(env_file=".env.test", extra="ignore")

def get_settings() -> Settings:
    """
    Returns the appropriate settings class based on the ENVIRONMENT variable.
    """
    env = os.getenv("ENVIRONMENT", "dev")
    if env == "test":
        return TestSettings()
    return Settings()

settings = get_settings()