import json


def evaluate_verdict(accuracy, relevance, hallucination, completeness):

    accuracy_score = accuracy.get("score", 0)
    relevance_score = relevance.get("score", 0)
    hallucination_score = hallucination.get("score", 0)
    completeness_score = completeness.get("score", 0)

    overall_score = round(
        (
            accuracy_score +
            relevance_score +
            hallucination_score +
            completeness_score
        ) / 4
    )

    if overall_score >= 80:
        verdict = "Pass"

    elif overall_score >= 60:
        verdict = "Needs Improvement"

    else:
        verdict = "Fail"

    summary = (
        f"The response achieved an overall score of {overall_score}. "
        f"Accuracy={accuracy_score}, "
        f"Relevance={relevance_score}, "
        f"Hallucination={hallucination_score}, "
        f"Completeness={completeness_score}."
    )

    return {
        "overall_score": overall_score,
        "verdict": verdict,
        "summary": summary
    }