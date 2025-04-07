# azure_openai_client.py
import os
from openai import AsyncAzureOpenAI, AzureOpenAI
from custom_agents.config import settings


class AzureOpenAIClient:
    @staticmethod
    def create_async_client():
        return AsyncAzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
        )
    
    @staticmethod
    def create_client():
        return AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
        )