# social_checker.py
from urllib.parse import quote

def generate_dorks(local_number: str):
    """
    Génère des Google Dorks pour divers réseaux sociaux et sites Ivoiriens.
    """
    # Ensure local number is in 10-digit format if possible
    if len(local_number) == 9 and not local_number.startswith('0'):
        local_number = '0' + local_number

    # Dorks de base
    dorks = {
        "tiktok": f'"{local_number}" site:tiktok.com',
        "facebook": f'"{local_number}" site:facebook.com',
        "instagram": f'"{local_number}" site:instagram.com',
        "linkedin": f'"{local_number}" site:linkedin.com',
        "twitter": f'"{local_number}" site:twitter.com',
    }

    # Dorks spécifiques CI
    ci_dorks = {
        "abidjan_net": f'"{local_number}" site:abidjan.net',
        "coinafrique": f'"{local_number}" site:coinafrique.ci',
        "jumia_deals": f'"{local_number}" site:deals.jumia.ci',
        "annuaire_ci": f'"{local_number}" site:annuaireci.com',
    }

    dorks.update(ci_dorks)

    results = {}
    for platform, dork in dorks.items():
        google_url = f"https://www.google.com/search?q={quote(dork)}"
        results[platform] = {"checked": False, "dork": dork, "dork_url": google_url}
    return results

def search_name(local_number: str):
    """
    Génère des dorks spécifiquement pour tenter de trouver un nom associé.
    """
    # Ensure local number is in 10-digit format if possible
    if len(local_number) == 9 and not local_number.startswith('0'):
        local_number = '0' + local_number

    name_dorks = {
        "facebook_name": f'site:facebook.com "{local_number}"',
        "truecaller_web": f'site:truecaller.com "{local_number}"',
        "general_name": f'"{local_number}" (nom OR name OR "appelez-moi")',
    }

    results = {}
    for platform, dork in name_dorks.items():
        google_url = f"https://www.google.com/search?q={quote(dork)}"
        results[platform] = {"dork": dork, "dork_url": google_url}
    return results

# ---- WhatsApp ----
def check_whatsapp(e164_number: str):
    link = f"https://wa.me/{e164_number.replace('+','')}"
    return {
        "checked": True,
        "found": "unknown",
        "link": link,
        "note": "wa.me permet d'ouvrir une discussion si le compte existe.",
    }

# ---- Telegram ----
def check_telegram(e164_number: str):
    link = f"https://t.me/{e164_number}"
    return {
        "checked": True,
        "found": "unknown",
        "link": link,
        "note": "t.me permet de contacter l'utilisateur si le compte existe.",
    }

# ---- Fonction globale ----
def check_all(e164_number: str, local_number: str):
    result = {}

    # WhatsApp & Telegram
    result["whatsapp"] = check_whatsapp(e164_number)
    result["telegram"] = check_telegram(e164_number)

    # Google Dorks (Social & CI)
    dorks = generate_dorks(local_number)
    for k, v in dorks.items():
        result[k] = v

    # Name Search Dorks
    name_info = search_name(local_number)
    result["name_search"] = name_info

    return result

if __name__ == "__main__":
    res = check_all("+2250707777777", "0707777777")
    import json
    print(json.dumps(res, indent=4))
