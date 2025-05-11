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
    print(f"-- Generating embedding for text length: {len(text)}")
    response = openai.embeddings.create(
        model=settings.embedding_3_small_deployment,
        input=text
    )
    print(f"-- Embedding response: {response.usage}")
    token_text_ratio = response.usage.total_tokens / len(text) 
    return response.data[0].embedding, token_text_ratio