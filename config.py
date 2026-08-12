import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RISK_MATRIX_PATH = BASE_DIR / "data" / "risk_matrix.json"


def _load_risk_matrix():
    if RISK_MATRIX_PATH.exists():
        with open(RISK_MATRIX_PATH, "r", encoding="utf-8") as handle:
            return json.load(handle)

    return {
        "Secrecy": {"score": 95, "priority": "CRITICAL"},
        "Market Manipulation / Misconduct": {"score": 100, "priority": "CRITICAL"},
        "Market Bribery": {"score": 98, "priority": "CRITICAL"},
        "Change in communication": {"score": 70, "priority": "MEDIUM"},
        "Complaints": {"score": 55, "priority": "LOW"},
        "Employee ethics": {"score": 85, "priority": "MEDIUM"},
        "No Compliance Risk": {"score": 0, "priority": "LOW"},
    }


RISK_MATRIX = _load_risk_matrix()