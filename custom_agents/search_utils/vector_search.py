from typing import List
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever  

import os
from custom_agents.config import settings
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


class AzureSearchRetriever(BaseRetriever):
    """
    AzureSearchRetriever retrieves documents from an Azure Search index.
    It uses the Azure Search client to perform the search and return the top k results.
    """
    k: int = 5
    credential: AzureKeyCredential = AzureKeyCredential(settings.azure_search_api_key)
    search_client: SearchClient = SearchClient(
        endpoint=settings.azure_search_service_endpoint,
        index_name=settings.azure_search_index_name,
        credential=credential
    )

    def get_relevant_documents(self, query: str) -> List[Document]:
        results = self.search_client.search(search_text=query, top=self.k)
        docs: List[Document] = []
        for r in results:
            docs.append(
                Document(
                    page_content=r["data"],
                    metadata={"company": r["companyname"], "year": r["year"], "tenkpage": r["tenkpage"], "metadata": r["metadata"]},
                )
            )
        return docs
