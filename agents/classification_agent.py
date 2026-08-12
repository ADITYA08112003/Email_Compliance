import re

from llm.model import get_llm
from utils.risk_matrix import get_risk


def _rule_based_classification(email):
    normalized = re.sub(r"\s+", " ", email).strip().lower()

    keyword_groups = {
        "Secrecy": [
            ("confidential", 3),
            ("confidentiality", 3),
            ("disclose", 3),
            ("disclosure", 3),
            ("secret", 2),
            ("sensitive", 2),
            ("private", 2),
            ("restricted", 2),
            ("password", 2),
            ("access", 1),
            ("non disclosure", 3),
            ("non-disclosure", 3),
        ],
        "Market Manipulation / Misconduct": [
            ("trading", 3),
            ("trade", 3),
            ("hedge", 3),
            ("hedging", 3),
            ("derivative", 3),
            ("swap", 3),
            ("options", 2),
            ("market", 2),
            ("financial", 2),
            ("investment", 2),
            ("commodity", 2),
            ("insider", 3),
        ],
        "Market Bribery": [
            ("bribe", 4),
            ("bribery", 4),
            ("kickback", 4),
            ("gift", 3),
            ("payment", 2),
            ("inducement", 3),
            ("cash", 2),
            ("favor", 2),
            ("influence", 2),
            ("incentive", 2),
        ],
        "Change in communication": [
            ("whatsapp", 2),
            ("phone", 2),
            ("call", 2),
            ("contact", 2),
            ("address", 2),
            ("message", 1),
            ("conversation", 1),
            ("later", 1),
            ("follow up", 2),
            ("new contact", 2),
        ],
        "Complaints": [
            ("complaint", 4),
            ("complaints", 4),
            ("concern", 2),
            ("issue", 2),
            ("problem", 2),
            ("incident", 2),
            ("grievance", 3),
            ("escalation", 3),
            ("loss of information", 4),
            ("prevent loss", 3),
        ],
        "Employee ethics": [
            ("ethics", 4),
            ("ethical", 4),
            ("inappropriate", 3),
            ("social", 2),
            ("drinks", 3),
            ("harassment", 4),
            ("misconduct", 3),
            ("unprofessional", 3),
            ("conduct", 2),
            ("personal", 2),
            ("offensive", 3),
        ],
    }

    matched_terms = {}
    scores = {}

    for category, terms in keyword_groups.items():
        matched = []
        score = 0
        for term, weight in terms:
            if term in normalized:
                matched.append(term)
                score += weight
        if score > 0:
            matched_terms[category] = matched
            scores[category] = score

    if not scores:
        return None

    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]

    if best_score < 3:
        return None

    benign_context = [
        "thank you",
        "thanks",
        "please",
        "signed",
        "fax",
        "records",
        "appropriate party",
        "migration",
        "outlook",
        "button",
        "save my data",
        "calendar",
        "contacts",
        "resolution center",
        "meeting",
        "team",
        "project",
    ]

    suspicious_context = [
        "do not disclose",
        "unauthorized",
        "third party",
        "without consent",
        "steal",
        "leak",
        "improper",
        "unapproved",
        "drinks",
        "personal",
        "social",
        "hedging",
        "derivative",
        "swap",
        "trade",
        "bribe",
        "kickback",
    ]

    if best_category == "Secrecy":
        if any(marker in normalized for marker in benign_context) and not any(marker in normalized for marker in suspicious_context):
            classification = "False Positive"
        else:
            classification = "True Positive" if best_score >= 6 else "False Positive"
    elif best_category == "Complaints":
        classification = "False Positive" if any(marker in normalized for marker in ["migration", "outlook", "button", "calendar", "contacts", "resolution center"]) else "True Positive"
    elif best_category == "Change in communication":
        classification = "True Positive" if any(marker in normalized for marker in ["market", "weakness", "whatsapp", "call", "phone", "address", "contact", "later"]) else "False Positive"
    elif best_category == "Employee ethics":
        classification = "True Positive" if any(marker in normalized for marker in ["drinks", "personal", "social", "inappropriate", "harassment"]) else "False Positive"
    else:
        classification = "True Positive" if best_score >= 6 else "False Positive"

    risk = get_risk(best_category)
    reason = f"The email contains compliance-related language such as: {', '.join(matched_terms[best_category][:3])}."

    return f"""Category: {best_category}
Reason: {reason}
Risk Score: {risk['score']}
Classification: {classification}
Priority: {risk['priority']}"""


def classify_email(email, retrieved_context):
    rule_result = _rule_based_classification(email)
    if rule_result:
        return rule_result

    llm = get_llm()

    prompt = f"""
You are a Compliance AI Assistant for employee communication surveillance.

Analyze the following email and decide whether it represents a potential compliance issue.

Allowed categories:
- Secrecy
- Market Manipulation / Misconduct
- Market Bribery
- Change in communication
- Complaints
- Employee ethics
- No Compliance Risk

Email:
{email}

Retrieved Compliance Examples:
{retrieved_context}

Return a concise structured response with the following fields:
1. Category
2. Reason
3. Risk Score
4. Classification (True Positive or False Positive)
5. Priority

Rules:
- Use No Compliance Risk when the email appears benign and does not indicate misconduct, bribery, confidentiality concerns, or ethical issues.
- If the email is clearly about confidential information, sensitive business data, or trading-related behavior, favor the most relevant compliance category.
- For false positives, explain why the email was not treated as a compliance concern.
- For true positives, cite the suspicious behavior or content that supports the category.
"""

    response = llm.invoke(prompt)
    return response.content