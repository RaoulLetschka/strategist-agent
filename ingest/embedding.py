import openai
from custom_agents.config import settings
# Configure OpenAI for Azure.
openai.api_type = "azure"
openai.api_key = settings.azure_openai_api_key
openai.azure_endpoint = settings.azure_openai_endpoint
openai.api_version = settings.azure_openai_api_version

def generate_embedding(text: str):
    """
    Generates an embedding for a given text input using Azure OpenAI.
    
    Parameters:
        text (str): The text to embed.
    
    Returns:
        List[float]: The embedding vector.
    """
    response = openai.embeddings.create(
        model=settings.embedding_3_small_deployment,
        input=text
    )
    # print(f"Embedding response: {response.data[0].embedding}")
    return response.data[0].embedding