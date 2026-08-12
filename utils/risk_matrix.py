from config import RISK_MATRIX


def get_risk(category):

    return RISK_MATRIX.get(

        category,

        {

            "score": 0,

            "priority": "LOW"

        }

    )