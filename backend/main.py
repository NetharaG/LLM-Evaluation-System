from fastapi import FastAPI
from pydantic import BaseModel

from rag.retrieval import retrieve

from agents.accuracy_agent import evaluate_accuracy
from agents.relevance_agent import evaluate_relevance
from agents.hallucination_agent import evaluate_hallucination
from agents.completeness_agent import evaluate_completeness
from agents.verdict_agent import evaluate_verdict

app = FastAPI(title="LLM Evaluation System")


class EvaluationRequest(BaseModel):
    question: str
    ai_response: str
class BatchEvaluationRequest(BaseModel):
    evaluations: list[EvaluationRequest]


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

    completeness = evaluate_completeness(
        data.question,
        data.ai_response,
        reference_answer
    )

    verdict = evaluate_verdict(
    accuracy,
    relevance,
    hallucination,
    completeness
)
    print("Question:", data.question)
    print("Reference:", reference_answer)
    print("AI Response:", data.ai_response)
    print("-" * 60)

    return {
        "status": "success",

        "question": data.question,

        "ai_response": data.ai_response,

        "reference_answer": reference_answer,

        "category": category,

        "accuracy": accuracy,

        "relevance": relevance,

        "hallucination": hallucination,

        "completeness": completeness,

        "verdict": verdict
    }

@app.post("/batch_evaluate")
def batch_evaluate(data: BatchEvaluationRequest):

    results = []

    for item in data.evaluations:

        # Retrieve reference information
        retrieved = retrieve(item.question)

        reference_answer = retrieved["reference_answer"]
        retrieved_question = retrieved["question"]
        category = retrieved["category"]

        # Run Accuracy Agent
        accuracy = evaluate_accuracy(
            retrieved_question,
            reference_answer,
            item.ai_response
        )

        # Run Relevance Agent
        relevance = evaluate_relevance(
            retrieved_question,
            reference_answer,
            item.ai_response
        )

        # Run Hallucination Agent
        hallucination = evaluate_hallucination(
            retrieved_question,
            reference_answer,
            item.ai_response
        )

        # Run Completeness Agent
        completeness = evaluate_completeness(
            item.question,
            item.ai_response,
            reference_answer
        )

        # Run Verdict Agent
        verdict = evaluate_verdict(
            accuracy,
            relevance,
            hallucination,
            completeness
        )

        # Store result
        results.append({
            "question": item.question,
            "ai_response": item.ai_response,
            "reference_answer": reference_answer,
            "category": category,
            "accuracy": accuracy,
            "relevance": relevance,
            "hallucination": hallucination,
            "completeness": completeness,
            "verdict": verdict
        })

    return {
        "status": "success",
        "total_records": len(results),
        "results": results
    }