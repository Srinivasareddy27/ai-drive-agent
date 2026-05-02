def apply_guardrails(answer, context):
    if not answer:
        return "Answer not found in documents"

    if answer.lower() not in context.lower():
        return "Answer not found in documents"

    return answer