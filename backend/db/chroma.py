import chromadb

# Initialize ChromaDB in persistent mode (saves data locally)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create (or load) a collection named "code_samples"
code_collection = chroma_client.get_or_create_collection(name="code_samples")

def add_code_sample(id: str, code: str, embedding: list[float]):
    """
    Stores a code snippet with its embedding in ChromaDB.

    Args:
        id (str): A unique identifier for the code snippet.
        code (str): The actual code snippet.
        embedding (list[float]): The embedding (vector representation) of the code.

    Returns:
        None
    """
    code_collection.add(ids=[id], embeddings=[embedding], metadatas=[{"code": code}])

def search_code_sample(query_embedding: list[float], top_k: int = 3):
    """
    Finds the top-k most similar code samples in the database.

    Args:
        query_embedding (list[float]): The embedding of the query code.
        top_k (int): The number of closest matches to return.

    Returns:
        dict: A dictionary containing the search results.
    """
    results = code_collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results
