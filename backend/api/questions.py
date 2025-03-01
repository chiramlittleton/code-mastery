from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
import chromadb

from backend.db.chroma import add_code_sample

router = APIRouter()

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
question_collection = chroma_client.get_or_create_collection(name="user_questions")

class QuestionRequest(BaseModel):
    language: str  # Programming language (Python, JavaScript, etc.)

@router.post("/generate/")
def generate_question(request: QuestionRequest):
    """
    Generates a programming challenge based on the selected language.
    """
    try:
        prompt = f"Generate a beginner-level coding problem in {request.language}. Provide the problem in a structured format."

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )

        question = response["choices"][0]["message"]["content"]

        # Store the question in ChromaDB
        question_collection.add(
            ids=[question],
            embeddings=[[0] * 1536],  # Placeholder embedding
            metadatas=[{"question": question, "language": request.language}]
        )

        return {"question": question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

