import ollama
import json

from agents.prompts import (
    ACCURACY_PROMPT,
    RELEVANCE_PROMPT,
    HALLUCINATION_PROMPT
)

MODEL_NAME = "llama3:latest"


def judge(criterion, question, reference_answer, ai_response):

    # Select Prompt
    if criterion == "Accuracy":
        system_prompt = ACCURACY_PROMPT

    elif criterion == "Relevance":
        system_prompt = RELEVANCE_PROMPT

    elif criterion == "Hallucination":
        system_prompt = HALLUCINATION_PROMPT

    else:
        system_prompt = "You are an evaluation judge."

    # User Prompt
    user_prompt = f"""
Question:
{question}

Reference Answer:
{reference_answer}

AI Response:
{ai_response}
"""

    # Call Ollama
    response = ollama.chat(
        model=MODEL_NAME,
        format="json",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    output = response["message"]["content"].strip()

    try:
        result = json.loads(output)
        return result

    except json.JSONDecodeError:

        return {
            "agent": criterion,
            "score": 0,
            "reason": "LLM returned invalid JSON."
        }


if __name__ == "__main__":

    result = judge(
        criterion="Accuracy",
        question="What happens if you eat watermelon seeds?",
        reference_answer="The watermelon seeds pass through your digestive system.",
        ai_response="Nothing happens. The seeds pass through your digestive system."
    )

    print(result)