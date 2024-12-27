import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str = "database_sqlite3"
    SECRET_KEY:str = "CNdgZiUU0qnKTg30Cj0wwy-Y6hCAqfdKCmSsICUhjBk"
    ALGORITHM: str = "HS256"
    CHAT_ID: int = 1617521485
    API_TOKEN: str = "7287309483:AAE7uiVbIH8p6VqojWH6SsF6XBlDXFIYxj8"
    # JWT_SECRET_KEY: str
    # JWY_ALGORITHM: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: int


    @property
    def DB_URL(self):
        return f"sqlite:///{self.DB_NAME}"

    #model_config = SettingsConfigDict(env_file=".env")
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = 'utf-8'

settings = Settings()
