from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "CHANGE_ME"
    PORT: int = 6100

    DB_USERNAME: str = "admin"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "db_auth_npk"
    DB_PORT: int = 6101
    DB_NAME: str = "postgres"

    # время жизни access-токен
    ACCESS_HOURS: int = 100
    # время жизни refresh, если потребуется
    REFRESH_DAYS: int | None = None  # 30

    #  CORS (нужно для Flutter Web)
    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

settings = Settings()
