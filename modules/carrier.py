# Plan national de numérotation à 10 chiffres (PNN10) en Côte d'Ivoire (depuis le 31 janvier 2021)
# Mobile: 01 (Moov), 05 (MTN), 07 (Orange)
# Fixe: 21 (Moov), 25 (MTN), 27 (Orange)

OPERATORS = {
    "01": {"operator": "Moov Africa", "line_type": "Mobile"},
    "05": {"operator": "MTN CI", "line_type": "Mobile"},
    "07": {"operator": "Orange CI", "line_type": "Mobile"},
    "21": {"operator": "Moov Africa", "line_type": "Fixe"},
    "25": {"operator": "MTN CI", "line_type": "Fixe"},
    "27": {"operator": "Orange CI", "line_type": "Fixe"},
}

FIXE_REGIONS = {
    "20": "Abidjan Plateau",
    "21": "Abidjan Sud",
    "22": "Cocody",
    "23": "Yopougon",
    "24": "Abobo",
    "30": "Yamoussoukro",
    "31": "Bouaké",
    "32": "Daloa",
    "33": "Man",
    "34": "San-Pédro",
    "35": "Abengourou",
    "36": "Korhogo",
}


def get_carrier(number: str):
    # Nettoyage
    clean_number = number.replace("+225", "").replace(" ", "").replace("-", "")

    # Gestion du format local à 10 chiffres
    if len(clean_number) == 10:
        pass
    elif len(clean_number) == 8:
        return {"error": "Ancien format à 8 chiffres détecté. Veuillez utiliser le nouveau format à 10 chiffres (+225 XX XX XX XX XX)."}
    elif len(clean_number) < 10:
        return {"error": "Numéro trop court pour la Côte d'Ivoire (10 chiffres requis)."}

    head_digits = clean_number[0:2]
    operator_info = OPERATORS.get(head_digits)
    if not operator_info:
        return {"error": f"Préfixe '{head_digits}' inconnu pour le plan à 10 chiffres de la Côte d'Ivoire."}

    line_type = operator_info.get("line_type", "Inconnu")
    operator_name = operator_info.get("operator", "Inconnu")

    region = None
    if line_type == "Fixe" and len(clean_number) >= 4:
        region = FIXE_REGIONS.get(clean_number[2:4], "Région inconnue")

    result = {
        "prefix": head_digits,
        "operator": operator_name,
        "line_type": line_type,
        "plan": "PNN 10 chiffres (Post-2021)",
        "portability_note": "Ce préfixe indique l'opérateur d'origine. La portabilité peut changer l'opérateur réel.",
    }

    if region:
        result["region"] = region

    return result
