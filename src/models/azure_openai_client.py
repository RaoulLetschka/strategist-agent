# azure_openai_client.py
from openai import AsyncAzureOpenAI
from src.config import settings

class AzureOpenAIClient:
    @staticmethod
    def create_client():
        return AsyncAzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
        )