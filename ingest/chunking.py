from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> list:
    """
    Splits the provided text into smaller chunks suitable for embedding.
    
    Parameters:
        text (str): The text to be chunked.
        chunk_size (int): Maximum number of characters per chunk.
        chunk_overlap (int): Number of overlapping characters between chunks.
    
    Returns:
        List[str]: A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    splitted_text = text_splitter.split_text(text)
    print(f"Text split into {len(splitted_text)} chunks")
    return splitted_text