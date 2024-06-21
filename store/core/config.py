from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Store API"
    ROOT_PATH: str = "/"
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_URL: str


settings = Settings()
