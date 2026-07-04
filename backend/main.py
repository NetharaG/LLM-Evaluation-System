from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="LLM Evaluation System")

class EvaluationRequest(BaseModel):
    question: str
    ai_response: str
    reference_answer: str = ""

@app.get("/")
def home():
    return {"message": "LLM Evaluation Backend Running"}

@app.post("/evaluate")
def evaluate(data: EvaluationRequest):
    return {
        "status": "success",
        "question": data.question,
        "ai_response": data.ai_response,
        "reference_answer": data.reference_answer
    }