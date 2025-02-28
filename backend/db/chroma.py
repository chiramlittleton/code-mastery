import chromadb
import openai

from backend.openai_config import configure_openai
from backend.db.openai_client import generate_code_variations

# Initialize ChromaDB in persistent mode (saves data locally)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create (or load) a collection named "code_samples"
code_collection = chroma_client.get_or_create_collection(name="code_samples", metadata={"hnsw:space": "cosine"}, embedding_function=None)

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


def add_code_sample(id: str, code: str, add_variations: bool = True):
    """
    Generates variations of a code snippet, embeds all, and stores them in ChromaDB.

    Args:
        id (str): A unique identifier for the original code.
        code (str): The original code snippet.
        add_variations (bool): Whether or not to add AI generated variations

    Returns:
        dict: Confirmation message with the number of variations added.
    """
    # Generate variations if enabled
    variations = generate_code_variations(code, num_variations=5) if add_variations else []

    # Include original snippet
    all_snippets = [code] + variations

    # Generate embeddings for all snippets
    embeddings = [
        openai.embeddings.create(model="text-embedding-ada-002", input=snippet).data[0].embedding
        for snippet in all_snippets
    ] 

    # Store all versions in ChromaDB
    for i, snippet in enumerate(all_snippets):
        code_collection.add(
            ids=[f"{id}_var{i}"],
            embeddings=[embeddings[i]],
            metadatas=[{"code": snippet, "variation": i}]
        )

    return {"message": f"Stored {len(all_snippets)} versions of the code snippet."}
