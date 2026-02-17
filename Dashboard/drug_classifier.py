import re

DOSAGE_FORMS = "tablet|tab|capsule|cap|ointment|cream|gel|solution|suspension|syrup|inj|injection|patch|spray|powder|lotion|drop|drops|aerosol|foam|shampoo"
UNITS = "mg|mcg|g|gm|ml|l|%|iu"
SALT_FORMS = "hcl|hydrochloride|acetate|sodium|potassium|phosphate|calcium|magnesium"
CHEMICAL_SUFFIXES = "ine|ol|ate|ide|ium|one|ene|acid|azole|mycin|vir|statin|pril|sartan|cillin|lukast|oxetine|prazole|afil"
BRAND_KEYWORDS = "ellipta|diskus|turbuhaler|flexhaler|respimat|kwikpen|sensoready|autoinjector|pen|ultra|one touch|glucometer"

def classify_drug(drug_name):

    name = str(drug_name).lower()
    cleaned = re.sub(rf"\b({DOSAGE_FORMS}|{UNITS})\b", " ", name)
    cleaned = re.sub(r"\d+(\.\d+)?", " ", cleaned)
    cleaned = cleaned.replace("%", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    tokens = re.split(r"[ \-/]", cleaned)
    tokens = [t for t in tokens if t]

    if not tokens:
        return "Brand"

    first_token = tokens[0]

    if re.search(rf"\b({BRAND_KEYWORDS})\b", cleaned):
        return "Brand"

    for suffix in CHEMICAL_SUFFIXES.split("|"):
        if first_token.endswith(suffix):
            return "Generic"

    for salt in SALT_FORMS.split("|"):
        if re.search(rf"\b{salt}\b", cleaned):
            return "Generic"

    return "Brand"
