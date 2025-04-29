from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "auth-service"
    ENVIRONMENT: str = "dev"
    LOG_LEVEL: str = "INFO"

    AZURE_TENANT_ID: str
    AZURE_CLIENT_ID: str
    AZURE_CLIENT_SECRET: str
    KEYVAULT_URI: str
    SECRET_NAME: str

    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30

    APPINSIGHTS_CONNECTION_STRING: str | None = None

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

settings = Settings()