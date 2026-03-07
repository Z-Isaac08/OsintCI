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
    # Nettoyage basique
    clean_number = number.replace("+225", "")
    if len(clean_number) < 2:
        return {"error": "Numéro trop court pour déterminer le préfixe."}

    head_digits = clean_number[0:2]
    operator_info = OPERATORS.get(head_digits)
    if not operator_info:
        return {"error": "Préfixe inconnu pour la Côte d'Ivoire."}

    line_type = operator_info.get("line_type", "Inconnu")
    operator_name = operator_info.get("operator", "Inconnu")

    region = None
    if line_type == "Fixe" and len(clean_number) >= 4:
        region = FIXE_REGIONS.get(clean_number[2:4], "Région inconnue")

    result = {
        "prefix": head_digits,
        "operator": operator_name,
        "line_type": line_type,
        "portability_note": "Ce préfixe indique l'opérateur d'origine, pas forcément l'opérateur actuel.",
    }

    if region:
        result["region"] = region

    return result
