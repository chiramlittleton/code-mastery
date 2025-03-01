from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai

router = APIRouter()

class SolutionRequest(BaseModel):
    question: str
    user_solution: str

@router.post("/evaluate/")
def evaluate_solution(request: SolutionRequest):
    """
    Evaluates a user's solution and provides feedback.
    """
    try:
        prompt = f"Here is a coding problem: {request.question}\n\nHere is a user's solution:\n{request.user_solution}\n\nEvaluate the solution. Is it correct? If incorrect, explain why and suggest an improvement."

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )

        feedback = response["choices"][0]["message"]["content"]

        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

