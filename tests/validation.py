import pandas as pd

from agents.accuracy_agent import evaluate_accuracy
from agents.relevance_agent import evaluate_relevance
from agents.hallucination_agent import evaluate_hallucination


test_cases = [

    {
        "question": "What happens if you eat watermelon seeds?",
        "reference": "The watermelon seeds pass through your digestive system.",
        "response": "Nothing happens. The seeds pass through your digestive system."
    },

    {
        "question": "Who invented the telephone?",
        "reference": "Alexander Graham Bell invented the telephone.",
        "response": "Thomas Edison invented the telephone."
    },

    {
        "question": "What is photosynthesis?",
        "reference": "Photosynthesis is the process by which plants prepare food using sunlight.",
        "response": "Photosynthesis is the process by which plants make food using sunlight."
    },

    {
        "question": "What is the capital of India?",
        "reference": "New Delhi is the capital of India.",
        "response": "New Delhi is the capital of India."
    },

    {
        "question": "Why is the sky blue?",
        "reference": "The sky appears blue because sunlight is scattered by molecules in Earth's atmosphere.",
        "response": "The sky is blue because sunlight is scattered by the atmosphere."
    },

    {
        "question": "Which is the largest ocean?",
        "reference": "The Pacific Ocean is the largest ocean on Earth.",
        "response": "The Pacific Ocean is the largest ocean."
    },

    {
        "question": "Who was the first person to walk on the Moon?",
        "reference": "Neil Armstrong was the first person to walk on the Moon.",
        "response": "Neil Armstrong first walked on the Moon in 1969."
    },

    {
        "question": "Can antibiotics treat viral infections?",
        "reference": "No. Antibiotics treat bacterial infections, not viral infections.",
        "response": "Antibiotics do not work against viruses."
    },

    {
        "question": "What is the boiling point of water?",
        "reference": "Water boils at 100°C at standard atmospheric pressure.",
        "response": "Water boils at 100 degrees Celsius at standard atmospheric pressure."
    },

    {
        "question": "What is Python programming?",
        "reference": "Python is a high-level programming language.",
        "response": "Bananas are yellow fruits."
    }

]

results = []

print("\n========== VALIDATION RESULTS ==========\n")

for i, test in enumerate(test_cases, start=1):

    print("=" * 70)
    print(f"Test Case {i}")
    print("=" * 70)

    print("Question:")
    print(test["question"])

    accuracy = evaluate_accuracy(
        test["question"],
        test["reference"],
        test["response"]
    )

    relevance = evaluate_relevance(
        test["question"],
        test["reference"],
        test["response"]
    )

    hallucination = evaluate_hallucination(
        test["question"],
        test["reference"],
        test["response"]
    )

    print("\nAccuracy")
    print(accuracy)

    print("\nRelevance")
    print(relevance)

    print("\nHallucination")
    print(hallucination)

    results.append({

        "Question": test["question"],

        "Accuracy Score": accuracy["score"],
        "Accuracy Reason": accuracy["reason"],

        "Relevance Score": relevance["score"],
        "Relevance Reason": relevance["reason"],

        "Hallucination Score": hallucination["score"],
        "Hallucination Reason": hallucination["reason"],

        "Hallucinated Statement":
            hallucination.get("hallucinated_statement", "None")

    })

    print("\n")


df = pd.DataFrame(results)

df.to_csv(
    "validation_results.csv",
    index=False
)

print("=" * 70)
print("Validation completed successfully.")
print("Results saved to validation_results.csv")
print("=" * 70)