from utils.parser import extract_category


def test_extract_category_from_structured_response():
    text = """
    After analyzing the email, I have determined the following:

    **Category:** Market Manipulation / Misconduct
    **Reason:** The email contains suspicious trading language.
    **Risk Score:** High
    **Classification:** True Positive
    **Priority:** High
    """

    assert extract_category(text) == "Market Manipulation / Misconduct"
