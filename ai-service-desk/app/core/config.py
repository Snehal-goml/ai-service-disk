from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Service Desk"
    API_VERSION: str = "v1"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite+aiosqlite:///./servicedesk.db"
    aws_secret_access_key: str = "demo-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
