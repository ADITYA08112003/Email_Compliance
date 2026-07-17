def classify_email(text):
    rules = [
        (
            [
                "save my data",
                "outlook migration",
                "trust signer",
                "migration date",
                "pop up",
                "abort, cancel or trust signer",
                "failed to click",
                "resolution center",
                "pre-migration",
                "migrate",
                "migration",
                "error",
            ],
            "Complaints",
            "Urgent migration or service issue detected",
        ),
        (
            [
                "confidential:",
                "intended for the recipient",
                "strictly forbidden to share",
                "if you received this message by mistake",
                "confidentiality notice",
            ],
            "Disclaimer",
            "Disclaimer or confidentiality notice detected",
        ),
        (
            [
                "confidential",
                "secret",
                "do not disclose",
                "sensitive information",
                "for your records",
                "faxed copy",
                "signature and faxing back",
                "agreement of confidentiality",
                "password basis",
                "access to the board",
                "authorise access",
                "authorize access",
                "password basis now",
                "password",
            ],
            "Secrecy",
            "Sensitive information leakage detected",
        ),
        (
            [
                "agreement",
                "service agreement",
                "mailing address",
                "communication update",
                "communication modification",
                "change in communication",
                "update to our agreement",
            ],
            "Change in communication",
            "Agreement or communication update detected",
        ),
        (
            [
                "whatsapp",
                "drinks on until i do",
                "internal employee communication",
                "colleague",
                "john, is access to the board",
            ],
            "Employee ethics",
            "Internal employee communication detected",
        ),
        (
            [
                "bribe",
                "payment",
                "illegal incentive",
                "compensation",
            ],
            "Market Bribery",
            "Possible illegal financial incentive",
        ),
        (
            [
                "trading",
                "market",
                "commodity",
                "hedge",
                "hedging",
                "swap",
                "jet fuel",
                "weather derivative",
                "crude",
                "fuel management",
                "financial swaps",
            ],
            "Market Manipulation / Misconduct",
            "Suspicious trading or market activity detected",
        ),
    ]

    for phrases, category, reason in rules:
        if any(phrase in text for phrase in phrases):
            return category, reason

    return "Employee ethics", "General internal communication"
