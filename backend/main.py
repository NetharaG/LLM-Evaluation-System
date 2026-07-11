from fastapi import FastAPI
from pydantic import BaseModel
from rag.retrieval import retrieve

app = FastAPI()

class EvaluationRequest(BaseModel):
    question: str
    ai_response: str

@app.post("/evaluate")
def evaluate(data: EvaluationRequest):

    reference = retrieve(data.question)

    return {
        "status": "success",
        "question": data.question,
        "ai_response": data.ai_response,
        "reference_answer": reference
    }