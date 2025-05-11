import openai
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.retrievers import BaseRetriever
from langchain.docstore.document import Document
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from .config import settings
from ingest.embedding import generate_embedding

class AzureSearchRetriever(BaseRetriever):
    """
    A custom retriever that queries your Azure Cognitive Search index.
    """
    def __init__(self, top_k: int = 3):
        self.top_k = top_k
        credential = AzureKeyCredential(settings.azure_search_api_key)
        self.search_client = SearchClient(endpoint=settings.azure_search_service_endpoint,
                                          index_name=settings.azure_search_index_name,
                                          credential=credential)
        self.embedding_fn = generate_embedding

    def get_relevant_documents(self, query: str):
        # Generate embedding for the query (for a true vector search, you would pass this to your search API)
        query_embedding = self.embedding_fn(query)
        # For this demonstration, we perform a simple text search.
        results = self.search_client.search(search_text=query, top=self.top_k)
        docs = []
        for result in results:
            docs.append(Document(page_content=result["content"], metadata={"id": result["id"]}))
        return docs

    async def aget_relevant_documents(self, query: str):
        return self.get_relevant_documents(query)

def create_rag_agent():
    """
    Creates and returns a RetrievalQA chain using LangChain.
    It configures the OpenAI LLM to use your Azure OpenAI Service.
    """
    # Configure the OpenAI client to use Azure.
    openai.api_type = "azure"
    openai.api_key = settings.azure_openai_api_key
    openai.azure_endpoint = settings.azure_openai_endpoint
    openai.api_version = settings.azure_openai_api_version

    # Initialize the LLM via LangChain.
    llm = OpenAI(deployment_name=settings.embedding_3_small_deployment, temperature=0)
    retriever = AzureSearchRetriever(top_k=3)
    qa_chain = RetrievalQA(llm=llm, retriever=retriever)
    return qa_chain

# # Example usage when running the module directly.
# if __name__ == "__main__":
#     agent = create_rag_agent()
#     query = "What were the risk factors mentioned in the 2021 filing?"
#     answer = agent.run(query)
#     print("Answer:", answer)