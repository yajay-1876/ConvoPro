import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    MONGO_DB_URL: str
    MONGO_DB_NAME: str
    OLLAMA_URL: str
    CONVOPRO_OLLAMA_MODELS: str

    class Config:
        env_file=".env"
        env_file_encoding="utf-8"

# Pydantic Settings precedence is typically:
#
# 1. Environment Variables (Windows/User/Machine)
# 2. .env file
# 3. Default values