from llm.model import get_llm


def explain_prediction(email, prediction):
    llm = get_llm()

    prompt = f"""
Explain why this email was classified as {prediction}.

Describe the main compliance signals in plain language and explain whether the email appears to be a true positive or a false positive.

Email:
{email}
"""

    response = llm.invoke(prompt)
    return response.content