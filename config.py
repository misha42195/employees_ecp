import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    SECRET_KEY:str
    ALGORITHM: str
    CHAT_ID: int
    API_TOKEN: str
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
