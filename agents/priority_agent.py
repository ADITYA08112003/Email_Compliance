from config import RISK_MATRIX


def assign_priority(category):

    if category in RISK_MATRIX:

        return RISK_MATRIX[category]

    return {

        "score": 0,

        "priority": "LOW"

    }