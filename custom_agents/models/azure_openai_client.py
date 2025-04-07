# azure_openai_client.py
import os
from openai import AsyncAzureOpenAI, AzureOpenAI
from custom_agents.config import settings


class AzureOpenAIClient:
    @staticmethod
    def create_async_client(deployment):
        return AsyncAzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
            azure_deployment=deployment,
        )
    
    @staticmethod
    def create_client(deployment):
        return AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_deployment=deployment,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
        )