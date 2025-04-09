# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

SWOT_CATEGORIES = ['STRENGHTS', 'WEAKNESSES', 'OPPORTUNITIES', 'THREATS']

class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str

    gpt4o_deployment: str
    gpt4o_mini_deployment: str
    o3_mini_deployment: str

    openai_api_key: str

    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()
