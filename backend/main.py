from fastapi import FastAPI
from pydantic import BaseModel

from rag.retrieval import retrieve

from agents.accuracy_agent import evaluate_accuracy
from agents.relevance_agent import evaluate_relevance
from agents.hallucination_agent import evaluate_hallucination

app = FastAPI(title="LLM Evaluation System")


class EvaluationRequest(BaseModel):
    question: str
    ai_response: str


@app.get("/")
def home():
    return {
        "message": "LLM Evaluation Backend Running"
    }


@app.post("/evaluate")
def evaluate(data: EvaluationRequest):

    # Retrieve reference information
    retrieved = retrieve(data.question)

    reference_answer = retrieved["reference_answer"]
    retrieved_question = retrieved["question"]
    category = retrieved["category"]

    # Run Accuracy Agent
    accuracy = evaluate_accuracy(
        retrieved_question,
        reference_answer,
        data.ai_response
    )

    # Run Relevance Agent
    relevance = evaluate_relevance(
        retrieved_question,
        reference_answer,
        data.ai_response
    )

    # Run Hallucination Agent
    hallucination = evaluate_hallucination(
        retrieved_question,
        reference_answer,
        data.ai_response
    )

    return {
        "status": "success",

        "question": data.question,

        "ai_response": data.ai_response,

        "reference_answer": reference_answer,

        "category": category,

        "accuracy": accuracy,

        "relevance": relevance,

        "hallucination": hallucination
    }