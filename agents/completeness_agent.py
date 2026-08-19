# import json
# import re
# import ollama

# from .prompts import COMPLETENESS_PROMPT


# def extract_json(text):
#     """
#     Extract the first valid JSON object from the model response.
#     """

#     # Remove markdown if present
#     text = text.replace("```json", "").replace("```", "").strip()

#     match = re.search(r"\{[\s\S]*\}", text)

#     if not match:
#         raise ValueError("No valid JSON found.")

#     json_text = match.group(0)

#     return json.loads(json_text)


# def evaluate_completeness(question, ai_answer, reference_answer):
#     """
#     Evaluate completeness using the Completeness Judge prompt.
#     """

#     prompt = f"""
# {COMPLETENESS_PROMPT}

# User Question:
# {question}

# Reference Answer:
# {reference_answer}

# AI Response:
# {ai_answer}
# """

#     response = ollama.chat(
#         model="llama3:latest",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         options={
#             "temperature": 0
#         }
#     )

#     try:

#         result = extract_json(response["message"]["content"])

#     except Exception:

#         print("===== COMPLETENESS RAW RESPONSE =====")
#         print(response["message"]["content"])
#         print("====================================")

#         result = {
#             "agent": "Completeness",
#             "score": 50,
#             "reason": "Unable to evaluate completeness.",
#             "missing_points": "Unknown"
#         }

#     return result
import json
import re
import os
from groq import Groq

from .prompts import COMPLETENESS_PROMPT


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# JSON EXTRACTION
# ============================================================

def extract_json(text):
    """
    Extract the first valid JSON object from the model response.
    """

    # Remove markdown if present
    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{[\s\S]*\}", text)

    if not match:
        raise ValueError("No valid JSON found.")

    json_text = match.group(0)

    return json.loads(json_text)


# ============================================================
# COMPLETENESS EVALUATION
# ============================================================

def evaluate_completeness(question, ai_answer, reference_answer):
    """
    Evaluate completeness using the Completeness Judge prompt.
    """

    prompt = f"""
{COMPLETENESS_PROMPT}

User Question:
{question}

Reference Answer:
{reference_answer}

AI Response:
{ai_answer}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        # model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    raw_response = response.choices[0].message.content

    try:

        result = extract_json(raw_response)

    except Exception:

        print("===== COMPLETENESS RAW RESPONSE =====")
        print(raw_response)
        print("====================================")

        result = {
            "agent": "Completeness",
            "score": 50,
            "reason": "Unable to evaluate completeness.",
            "missing_points": "Unknown"
        }

    return result