from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.api.questions import router as questions_router
from backend.api.submissions import router as submissions_router
from backend.openai_config import configure_openai

# Load API key
configure_openai()

# Environment Variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/codemastery")
VECTOR_DB_URL = os.getenv("VECTOR_DB_URL", "http://chromadb:8000")

# Initialize FastAPI app
app = FastAPI()

# ✅ Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routers
app.include_router(questions_router, prefix="/questions")
app.include_router(submissions_router, prefix="/submissions")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Adaptive Learning API!",
        "database_url": DATABASE_URL,
        "vector_db_url": VECTOR_DB_URL
    }
