import json
import os
import re

DATA_FILE = "data/spam_numbers.json"


def load_spam_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def normalize_number(number: str) -> str:
    clean = number.replace(" ", "").replace("-", "")
    if clean.startswith("00"):
        clean = "+" + clean[2:]
    elif len(clean) == 10 and not clean.startswith("+"):
        clean = "+225" + clean
    return clean


def is_suspicious_pattern(national_digits: str) -> tuple[bool, str]:
    """
    Analyse les 10 derniers chiffres uniquement.
    Retourne (suspicious: bool, reason: str)
    """
    # Chiffre répété plus de 6 fois
    if any(national_digits.count(d) > 6 for d in "0123456789"):
        return True, "Chiffre répété excessivement"

    # Séquence entièrement identique ex: 0000000000
    if len(set(national_digits)) == 1:
        return True, "Numéro composé d'un seul chiffre répété"

    # Séquence croissante ou décroissante ex: 0123456789
    if national_digits in "01234567890123456789":
        return True, "Séquence numérique croissante détectée"
    if national_digits in "98765432109876543210":
        return True, "Séquence numérique décroissante détectée"

    return False, ""


def check_spam(number: str) -> dict:
    """
    Vérifie si un numéro est dans la blacklist locale
    ou correspond à un pattern suspect.
    """
    spam_data = load_spam_data()
    clean = normalize_number(number)

    # Extraire les 10 derniers chiffres pour l'analyse de pattern
    national_digits = re.sub(r"\D", "", clean)[-10:]

    # Vérification blacklist
    in_blacklist = clean in spam_data
    blacklist_info = spam_data.get(clean, {})

    # Vérification pattern
    suspicious, pattern_reason = is_suspicious_pattern(national_digits)

    # Calcul score
    risk_score = 0
    if in_blacklist:
        risk_score += 90
    if suspicious:
        risk_score = max(risk_score, 40)

    risk_score = min(risk_score, 100)

    # Risk level
    if risk_score >= 80:
        risk_level = "High"
    elif risk_score >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "is_spam": in_blacklist or suspicious,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "database_match": in_blacklist,
        "report_type": blacklist_info.get("type", None),
        "reports_count": blacklist_info.get("reports", 0),
        "last_seen": blacklist_info.get("date", None),
        "suspicious_pattern": suspicious,
        "pattern_reason": pattern_reason if suspicious else None,
        "note": (
            f"Signalé {blacklist_info.get('reports', 0)} fois — {blacklist_info.get('type', 'inconnu')}"
            if in_blacklist
            else "Aucune correspondance dans la liste noire locale."
        ),
    }


def add_to_blacklist(number: str, report_type: str = "unknown") -> dict:
    """
    Ajoute ou met à jour un numéro dans la blacklist locale.
    """
    spam_data = load_spam_data()
    clean = normalize_number(number)

    if clean in spam_data:
        spam_data[clean]["reports"] += 1
        spam_data[clean]["date"] = __import__("datetime").date.today().isoformat()
        spam_data[clean]["type"] = report_type
        action = "updated"
    else:
        spam_data[clean] = {
            "type": report_type,
            "reports": 1,
            "date": __import__("datetime").date.today().isoformat(),
        }
        action = "added"

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(spam_data, f, indent=4, ensure_ascii=False)

    return {"action": action, "number": clean, "type": report_type}
