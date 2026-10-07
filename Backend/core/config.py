from pydantic_settings import BaseSettings, SettingsConfigDict

class  Settings(BaseSettings):
    DB_URL : str
    JWT_SECRET_KEY: str
    ALGORITHM : str = 'HS256'
    ACCESS_TOKEN_EXPIRY: int = 30
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )

settings = Settings()