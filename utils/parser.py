import re


def _clean_value(value):
    if not value:
        return ""

    value = value.strip()
    value = re.sub(r"\*\*", "", value)
    value = re.sub(r"\*", "", value)
    value = re.sub(r"`", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" .:-")


def _normalize_text(text):
    if not text:
        return ""

    normalized = text.replace("\r\n", "\n")
    normalized = re.sub(r"\*\*(.*?)\*\*", r"\1", normalized)
    normalized = re.sub(r"[*_`]+", "", normalized)
    return normalized


def extract_structured_fields(text):
    if not text:
        return {}

    normalized = _normalize_text(text)
    fields = {}

    for key in ["category", "risk score", "priority", "classification"]:
        pattern = rf"\b{re.escape(key)}\b\s*:\s*(.+)"
        match = re.search(pattern, normalized, re.IGNORECASE)
        if match:
            value = _clean_value(match.group(1))
            value = value.split("\n")[0]
            fields[key.replace(" ", "_")] = value

    return fields


def extract_category(text):
    fields = extract_structured_fields(text)

    if fields.get("category"):
        return fields["category"]

    for label in ["Category", "category"]:
        match = re.search(rf"{label}\s*:\s*(.+)", _normalize_text(text), re.IGNORECASE)
        if match:
            return _clean_value(match.group(1))

    return "No Compliance Risk"