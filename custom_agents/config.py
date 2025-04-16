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
    embedding_deployment: str
    embedding_3_small_deployment: str

    openai_api_key: str

    azure_search_service_endpoint: str
    azure_search_api_key: str
    azure_search_index_name: str

    azure_blob_connection_string: str
    azure_blob_container_name: str

    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()
