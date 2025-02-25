import pytest
import chromadb
import uuid  # To generate unique collection names

@pytest.fixture
def chroma_client():
    """
    Create a temporary ChromaDB client for testing.
    """
    return chromadb.PersistentClient(path="./test_chroma_db")

def generate_unique_collection_name():
    """Generate a unique collection name for each test."""
    return f"test_code_samples_{uuid.uuid4().hex[:8]}"  # Shortened unique ID

def test_chromadb_client_creation():
    """
    Test that a ChromaDB client can be created successfully.
    """
    try:
        client = chromadb.PersistentClient(path="./test_chroma_db")
        assert client is not None
    except Exception as e:
        pytest.fail(f"ChromaDB client creation failed: {e}")

def test_chromadb_store_code_sample(chroma_client):
    """
    Test that a code snippet can be stored in ChromaDB.
    """
    collection_name = generate_unique_collection_name()
    code_collection = chroma_client.get_or_create_collection(name=collection_name)

    test_id = "test_snippet_1"
    test_code = "print('Hello, world!')"
    test_embedding = [0.1, 0.2, 0.3, 0.4]

    code_collection.add(ids=[test_id], embeddings=[test_embedding], metadatas=[{"code": test_code}])
    results = code_collection.query(query_embeddings=[test_embedding], n_results=1)

    assert results["ids"] == [[test_id]]
    assert results["metadatas"] == [[{"code": test_code}]]

    # Cleanup
    chroma_client.delete_collection(name=collection_name)

def test_chromadb_search_code_sample(chroma_client):
    """
    Test searching for a stored code snippet.
    """
    collection_name = generate_unique_collection_name()
    code_collection = chroma_client.get_or_create_collection(name=collection_name)

    test_id = "test_snippet_2"
    test_code = "print('Hello, AI!')"
    test_embedding = [0.2, 0.3, 0.4, 0.5]

    code_collection.add(ids=[test_id], embeddings=[test_embedding], metadatas=[{"code": test_code}])
    results = code_collection.query(query_embeddings=[test_embedding], n_results=1)

    assert results["ids"] == [[test_id]]
    assert results["metadatas"] == [[{"code": test_code}]]

    # Cleanup
    chroma_client.delete_collection(name=collection_name)

def test_chromadb_search_multiple_results(chroma_client):
    """
    Test retrieving multiple similar snippets.
    """
    collection_name = generate_unique_collection_name()
    code_collection = chroma_client.get_or_create_collection(name=collection_name)

    code_collection.add(
        ids=["snippet_1", "snippet_2"],
        embeddings=[[0.1, 0.2, 0.3, 0.4], [0.15, 0.25, 0.35, 0.45]],
        metadatas=[{"code": "print('Snippet 1')"}, {"code": "print('Snippet 2')"}],
    )

    results = code_collection.query(query_embeddings=[[0.12, 0.22, 0.32, 0.42]], n_results=2)

    assert len(results["ids"][0]) == 2
    assert "snippet_1" in results["ids"][0]
    assert "snippet_2" in results["ids"][0]

    # Cleanup
    chroma_client.delete_collection(name=collection_name)

def test_chromadb_search_no_results(chroma_client):
    """
    Test searching when no relevant results exist.
    """
    collection_name = generate_unique_collection_name()
    code_collection = chroma_client.get_or_create_collection(name=collection_name)

    results = code_collection.query(query_embeddings=[[0.9, 0.9, 0.9, 0.9]], n_results=1)

    assert len(results["ids"]) == 1
    assert results["ids"][0] == []  # Expecting an empty result

    # Cleanup
    chroma_client.delete_collection(name=collection_name)
