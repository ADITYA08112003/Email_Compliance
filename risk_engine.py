from config import PRIORITY_MATRIX

def get_risk_score(category):
    return PRIORITY_MATRIX.get(category, 10)

def get_priority(score):

    if score >= 90:
        return "HIGH"
    elif score >= 60:
        return "MEDIUM"
    else:
        return "LOW"