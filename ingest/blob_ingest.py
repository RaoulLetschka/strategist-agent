from azure.storage.blob import BlobServiceClient
from bs4 import BeautifulSoup
from custom_agents.config import settings

def get_html_forms_from_blob():
    """
    Connects to the blob container and downloads all blobs.
    Returns a list of dictionaries with 'id' and 'content' keys.
    """
    blob_service_client = BlobServiceClient.from_connection_string(settings.azure_blob_connection_string)
    container_client = blob_service_client.get_container_client(settings.azure_blob_container_name)
    
    documents = []
    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob)
        content = blob_client.download_blob().readall().decode("utf-8")
        # Extract text using BeautifulSoup.
        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text(separator="\n")
        documents.append({
            "id": blob.name,
            "content": text
        })
    return documents

def upload_html_to_blob(blob_name: str, html_content: str):
    """
    Uploads HTML content as a blob to the configured container.
    """
    blob_service_client = BlobServiceClient.from_connection_string(settings.azure_blob_connection_string)
    container_client = blob_service_client.get_container_client(settings.azure_blob_container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(html_content, overwrite=True)
    print(f"Uploaded blob: {blob_name}")

def delete_blob(blob_name: str):
    """
    Deletes a blob from the configured container.
    """
    blob_service_client = BlobServiceClient.from_connection_string(settings.azure_blob_connection_string)
    container_client = blob_service_client.get_container_client(settings.azure_blob_container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.delete_blob()
    print(f"Deleted blob: {blob_name}")