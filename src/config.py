# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str = "2023-05-15"

    gpt4o_deployment: str
    gpt4o_mini_deployment: str

    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()
