import json
import os

DATA_FILE = "data/spam_numbers.json"

def load_spam_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def check_spam(number: str):
    """
    Check if a number is in the local spam database or matches suspicious patterns.
    """
    spam_list = load_spam_data()

    # Normalize number for comparison (assuming e164 or similar)
    clean_number = number.replace(" ", "").replace("-", "")
    if not clean_number.startswith("+"):
        if clean_number.startswith("00"):
            clean_number = "+" + clean_number[2:]
        elif len(clean_number) == 10:
            clean_number = "+225" + clean_number

    is_in_list = clean_number in spam_list

    risk_score = 0
    if is_in_list:
        risk_score = 90

    # Simple pattern based risk (example: many repeating digits)
    if any(clean_number.count(digit) > 6 for digit in "0123456789"):
        risk_score = max(risk_score, 40)

    risk_level = "Low"
    if risk_score >= 80:
        risk_level = "High"
    elif risk_score >= 40:
        risk_level = "Medium"

    return {
        "is_spam": is_in_list,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "database_match": is_in_list,
        "note": "Basé sur la liste noire locale et l'analyse de motifs." if is_in_list else "Aucune correspondance dans la liste noire locale."
    }
