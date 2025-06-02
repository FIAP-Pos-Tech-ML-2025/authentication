from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "auth-service"
    ENVIRONMENT: str = "dev"
    LOG_LEVEL: str = "INFO"

    AZURE_TENANT_ID: Optional[str] = None
    AZURE_CLIENT_ID: Optional[str] = None
    AZURE_CLIENT_SECRET: Optional[str] = None
    KEYVAULT_URI: Optional[str] = None
    SECRET_NAME: Optional[str] = None

    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    # Add a local signing key for MVP when Key Vault is not used
    JWT_LOCAL_SIGNING_KEY: str = "your-very-secret-and-strong-key-for-mvp"

    APPINSIGHTS_CONNECTION_STRING: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()