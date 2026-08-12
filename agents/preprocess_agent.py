import re


def clean_email(text):

    text = text.lower()

    text = re.sub(

        r"\s+",

        " ",

        text

    )

    return text.strip()