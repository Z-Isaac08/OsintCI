import phonenumbers
import re
from phonenumbers import geocoder, carrier, timezone
from phonenumbers.phonenumberutil import NumberParseException

PHONE_TYPE_MAP = {
    0: "Fixed line",
    1: "Mobile",
    2: "Fixed line or mobile",
    3: "Toll-free number",
    4: "Premium rate number",
    5: "Shared cost number",
    6: "VoIP / virtual number",
    7: "Personal number",
    8: "Pager",
    9: "Universal access number",
    10: "Voicemail",
    -1: "Unknown",
}


def analyze_number(raw_number: str):
    try:
        clean_number = re.sub(r"[^\d+]", "", raw_number)

        if clean_number.startswith("00225"):
            clean_number = "+" + clean_number[2:]

        parsed_number = phonenumbers.parse(clean_number, "CI")

        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)

        return {
            "valid": is_valid,
            "possible": is_possible,
            "country_code": parsed_number.country_code,
            "national_number": parsed_number.national_number,
            "e164": phonenumbers.format_number(
                parsed_number, phonenumbers.PhoneNumberFormat.E164
            ),
            "international": phonenumbers.format_number(
                parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            ),
            "carrier": carrier.name_for_number(parsed_number, "fr"),
            "region": geocoder.description_for_number(parsed_number, "fr"),
            "timezone": timezone.time_zones_for_number(parsed_number),
            "number_type": PHONE_TYPE_MAP.get(
                phonenumbers.number_type(parsed_number), "UNKNOWN"
            ),
        }

    except NumberParseException as e:
        return {"valid": False, "error": str(e)}
