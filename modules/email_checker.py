# email_checker.py
import re
from urllib.parse import quote

def generate_email_dorks(number: str):
    """
    Génère des dorks pour trouver des adresses email associées à un numéro.
    """
    # Normalize
    clean_number = number.replace(" ", "").replace("+", "")

    # Ensure local number is in 10-digit format if possible
    if len(clean_number) == 9 and not clean_number.startswith('0'):
        clean_number = '0' + clean_number

    dorks = {
        "email_discovery": f'"{clean_number}" "@gmail.com" OR "@yahoo.fr" OR "@outlook.com"',
        "contact_pages": f'"{clean_number}" "contact" OR "email" OR "courriel"',
        "leaks_check": f'"{clean_number}" "password" OR "leak" OR "database"'
    }

    results = {}
    for key, dork in dorks.items():
        results[key] = {
            "dork": dork,
            "url": f"https://www.google.com/search?q={quote(dork)}"
        }
    return results

def analyze_email(email: str):
    """
    Analyse basique d'une adresse email pour OSINT.
    """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {"error": "Format d'email invalide."}

    dorks = {
        "social_presence": f'"{email}" site:facebook.com OR site:linkedin.com OR site:twitter.com',
        "leaks": f'"{email}" leak OR database OR breachtalk',
        "mentions": f'"{email}" -site:google.com'
    }

    results = {
        "email": email,
        "dorks": {}
    }

    for key, dork in dorks.items():
        results["dorks"][key] = {
            "dork": dork,
            "url": f"https://www.google.com/search?q={quote(dork)}"
        }

    return results
