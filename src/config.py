
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: int
    DB_NAME: str
    COOKIE_SECRET: str
    PW_SECRET: str

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:123456@localhost:5432/BOSCH
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        # postgresql+asyncpg://postgres:123456@localhost:5432/BOSCH
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
