from agents.llm_judge import judge


def evaluate_relevance(question, reference_answer, ai_response):

    return judge(
        criterion="Relevance",
        question=question,
        reference_answer=reference_answer,
        ai_response=ai_response
    )
if __name__ == "__main__":

    result = evaluate_relevance(
        question="What happens if you eat watermelon seeds?",
        reference_answer="The watermelon seeds pass through your digestive system.",
        ai_response="Nothing happens. The seeds pass through your digestive system."
    )

    print(result)