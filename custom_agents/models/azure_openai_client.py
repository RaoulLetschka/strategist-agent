# azure_openai_client.py
import os
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI, AzureOpenAI

env_loaded = load_dotenv("../../.env")
print(os.getenv("AZURE_OPENAI_ENDPOINT"))

class AzureOpenAIClient:
    @staticmethod
    def create_async_client():
        return AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )
    
    @staticmethod
    def create_client():
        return AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )