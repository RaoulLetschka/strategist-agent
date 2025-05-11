from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField
)
from azure.core.credentials import AzureKeyCredential
from custom_agents.config import settings

def create_or_update_index(index_name: str, client: SearchIndexClient):
    """
    Creates (or updates) the Azure Cognitive Search index with a schema
    that supports document content and vector embeddings.
    """
    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        SearchableField(name="content", type="Edm.String"),
        # Store the embedding vector as a collection of single-precision floats.
        SimpleField(name="embedding", type="Edm.Collection(Edm.Single)")
    ]
    index = SearchIndex(name=index_name, fields=fields)
    result = client.create_or_update_index(index)
    print("Index created or updated:", result.name)
    return result

def upload_documents_to_index(documents: list):
    """
    Uploads the list of documents to the Azure Search index.
    Each document should include: id, content, and embedding.
    """
    credential = AzureKeyCredential(settings.azure_search_api_key)
    search_client = SearchClient(endpoint=settings.azure_search_service_endpoint,
                                 index_name=settings.azure_search_index_name,
                                 credential=credential)
    results = search_client.upload_documents(documents=documents)
    # print("Upload results:", results)

def delete_document_from_index(document_id: str):
    """
    Deletes a document from the Azure Search index by its ID.
    """
    credential = AzureKeyCredential(settings.azure_search_api_key)
    search_client = SearchClient(endpoint=settings.azure_search_service_endpoint,
                                 index_name=settings.azure_search_index_name,
                                 credential=credential)
    documents = [{"id": document_id}]
    result = search_client.delete_documents(key_field="id", documents=documents)
    print("Delete results:", result)