# social_checker.py
from urllib.parse import quote


def generate_dorks(local_number: str):
    """
    Génère des Google Dorks pour TikTok, Facebook et Instagram
    """
    dorks = {
        "tiktok": f'"{local_number}" site:tiktok.com',
        "facebook": f'"{local_number}" site:facebook.com',
        "instagram": f'"{local_number}" site:instagram.com',
    }

    results = {}
    for platform, dork in dorks.items():
        google_url = f"https://www.google.com/search?q={quote(dork)}"
        results[platform] = {"checked": False, "dork": dork, "dork_url": google_url}
    return results


# ---- WhatsApp ----
def check_whatsapp(e164_number: str):
    link = f"https://wa.me/{e164_number.replace('+','')}"
    # Note : impossible de vérifier réellement l'existence
    return {
        "checked": True,
        "found": "unknown",
        "link": link,
        "note": "wa.me ne permet pas de confirmer l'existence d'un compte.",
    }


# ---- Telegram ----
def check_telegram(e164_number: str):
    link = f"https://t.me/{e164_number}"
    # Note : impossible de vérifier réellement l'existence
    return {
        "checked": True,
        "found": "unknown",
        "link": link,
        "note": "t.me ne permet pas de confirmer l'existence d'un compte.",
    }


# ---- Fonction globale ----
def check_all(e164_number: str, local_number: str):
    result = {}

    # WhatsApp
    result["whatsapp"] = check_whatsapp(e164_number)

    # Telegram
    result["telegram"] = check_telegram(e164_number)

    # Google Dorks
    result.update(generate_dorks(local_number))

    return result


# ---- Exemple d'utilisation ----
if __name__ == "__main__":
    e164 = "+2250585456593"
    local = "0585456593"

    res = check_all(e164, local)
    import json

    print(json.dumps(res, indent=4, ensure_ascii=False))
