from llm.model import get_llm


def extract_evidence(email):
    llm = get_llm()

    prompt = f"""
Extract only the lines from the email that most strongly indicate a possible compliance issue.

Focus on direct evidence such as:
- confidentiality or secrecy requests
- trading or market-related language
- bribery or improper inducements
- unusual communication changes or suspicious requests
- employee conduct or ethics concerns

Email:
{email}

Return:
Evidence Lines
Reason
"""

    response = llm.invoke(prompt)
    return response.content