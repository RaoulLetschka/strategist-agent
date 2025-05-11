from ingest.blob_ingest import get_html_forms_from_blob
from ingest.chunking import chunk_text
from ingest.embedding import generate_embedding

def prepare_chunked_documents():
    """
    Retrieves HTML forms from blob storage, extracts text, splits into chunks,
    and computes embeddings for each chunk.
    
    Returns:
        List[dict]: A list of documents with unique id, content, and embedding.
    """
    html_docs = get_html_forms_from_blob()
    all_documents = []
    
    for doc in html_docs:
        # Each document from blob ingestion.
        chunks = chunk_text(doc["content"])
        for idx, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)
            # Create a unique ID for each chunk.
            document_id = f"{doc['id']}_{idx}"
            all_documents.append({
                "id": document_id,
                "content": chunk,
                "embedding": embedding
            })
    return all_documents
