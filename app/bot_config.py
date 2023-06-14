from pydantic import BaseSettings, SecretStr
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    bot_token: SecretStr
    bot_name: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()