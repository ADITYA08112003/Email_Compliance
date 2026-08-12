import streamlit as st

from agents.preprocess_agent import clean_email
from agents.retrieval_agent import retrieve_examples
from agents.classification_agent import classify_email
from agents.evidence_agent import extract_evidence
from agents.explanation_agent import explain_prediction
from utils.parser import extract_category
from utils.risk_matrix import get_risk


# -------------------------------
# Streamlit Page Configuration
# -------------------------------

st.set_page_config(

    page_title="Compliance AI Assistant",

    page_icon="📧",

    layout="wide"

)

st.title("Email Compliance")

# st.write(

#     "AI-powered communication surveillance for compliance use cases such as secrecy, market misconduct, bribery, and employee ethics."

# )

# st.caption(

#     "The risk matrix is configurable through the JSON file in data/risk_matrix.json without changing code."

# )

# -------------------------------
# Email Input
# -------------------------------

email = st.text_area(

    "Paste Employee Email",

    placeholder="Example: confidential information, trading-related language, bribery, or suspicious employee conduct",

    height=300

)

# -------------------------------
# Analyze Button
# -------------------------------

if st.button("Analyze Email"):

    if len(email.strip()) == 0:

        st.error("Please enter an email.")

    else:

        # -------------------------------
        # Step 1 : Clean Email
        # -------------------------------

        cleaned_email = clean_email(email)

        # -------------------------------
        # Step 2 : Retrieve Similar Examples
        # -------------------------------

        st.info("Searching Similar Emails...")

        retrieved = retrieve_examples(

            cleaned_email

        )

        context = ""

        if retrieved:
            context = "\n\n".join(item["document"] for item in retrieved)
        else:
            context = "No similar examples were found."

        # -------------------------------
        # Step 3 : LLM Classification
        # -------------------------------

        st.info("Classifying Email...")

        prediction = classify_email(

            cleaned_email,

            context

        )

        # -------------------------------
        # Step 4 : Extract Structured Fields
        # -------------------------------

        category = extract_category(prediction)

        # -------------------------------
        # Step 5 : Risk Matrix
        # -------------------------------

        risk = get_risk(category)

        # -------------------------------
        # Step 6 : Evidence Extraction
        # -------------------------------

        evidence = extract_evidence(

            cleaned_email

        )

        # -------------------------------
        # Step 7 : LLM Explanation
        # -------------------------------

        explanation = explain_prediction(

            cleaned_email,

            category

        )

        # -------------------------------
        # Display Output
        # -------------------------------

        st.success("Analysis Completed")

        st.subheader("Category")

        st.write(category)

        st.subheader("Risk Score")

        st.write(risk["score"])

        st.subheader("Priority")

        st.write(risk["priority"])

        st.subheader("LLM Prediction")

        st.write(prediction)

        st.subheader("Evidence")

        st.write(evidence)

        st.subheader("Explanation")

        st.write(explanation)

        # st.subheader("Retrieved Context")

        # if retrieved:
        #     for item in retrieved:
        #         st.markdown(f"- {item['document']}")
        # else:
        #     st.write(context)