from fastapi import FastAPI, HTTPException
from backend.openai_config import configure_openai 
from pydantic import BaseModel
from backend.db.chroma import add_code_sample, search_code_sample
from backend.db.openai_client import generate_code_variations

configure_openai()

app = FastAPI()

class CodeSnippet(BaseModel):
    id: str
    code: str
    add_variations: bool = True

class SearchRequest(BaseModel):
    query_embedding: list[float]
    top_k: int = 3

@app.get("/")
def read_root():
    return {"message": "Welcome to the Code Mastery API!"}

@app.post("/add-code/")
def add_code(request: CodeSnippet):
    """
    API endpoint to add a code snippet to ChromaDB.

    Request Body:
        - id (str): Unique identifier for the snippet.
        - code (str): The actual code snippet.
        - add_variations (bool): Whether AI-generated variations should be stored.

    Returns:
        dict: Confirmation message.
    """
    try:
        response = add_code_sample(request.id, request.code, request.add_variations)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search-code/")
def search_code(request: SearchRequest):
    """
    API endpoint to search for similar code snippets.

    Request Body:
        - query_embedding (list[float]): The embedding vector to search.
        - top_k (int): Number of closest matches to return.

    Returns:
        dict: Search results from ChromaDB.
    """
    try:
        results = search_code_sample(request.query_embedding, request.top_k)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
