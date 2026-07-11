from agents.llm_judge import judge


def evaluate_hallucination(question, reference_answer, ai_response):

    return judge(
        criterion="Hallucination",
        question=question,
        reference_answer=reference_answer,
        ai_response=ai_response
    )

if __name__ == "__main__":

    result = evaluate_hallucination(
        question="What happens if you eat watermelon seeds?",
        reference_answer="The watermelon seeds pass through your digestive system.",
        ai_response="Watermelon seeds grow into a watermelon tree inside your stomach."
    )

    print(result)  