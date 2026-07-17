from flask import Flask, render_template, request
from ai.preprocess import clean_email
from ai.classifier import classify_email
from ai.risk_engine import get_risk_score, get_priority
from config import CATEGORY_CLASSIFICATION

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":
        email = request.form["email"]

        cleaned = clean_email(email)

        category, reason = classify_email(cleaned)

        risk_score = get_risk_score(category)

        priority = get_priority(risk_score)

        classification = CATEGORY_CLASSIFICATION.get(
            category,
            "True Positive" if risk_score >= 60 else "False Positive"
        )

        result = {
            "email": email,
            "category": category,
            "reason": reason,
            "risk_score": risk_score,
            "priority": priority,
            "classification": classification
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
