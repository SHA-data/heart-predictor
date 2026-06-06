from PyPDF2 import PdfReader
import re

# Extract text from PDF and return as structured JSON
def text_extract(document):
    reader = PdfReader(document)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    normalized_text = normalize_text(full_text)
    return parse_medical_data(normalized_text)


def normalize_text(text):
    return re.sub(r'\s+', ' ', text).strip()


def find_field(text, labels, value_pattern=r'([\w%.,]+)', flags=re.I):
    escaped_labels = [re.escape(label) for label in labels]
    label_pattern = '|'.join(escaped_labels)
    regex = rf'(?:{label_pattern})(?:\s*\([^\)]*\))?\s*[:=\-]?\s*{value_pattern}'
    return re.search(regex, text, flags)


# Parse medical report text and return as JSON dictionary
def parse_medical_data(text):
    data = {
        "anaemia": None,
        "creatinine_phosphokinase": None,
        "diabetes": None,
        "ejection_fraction": None,
        "high_blood_pressure": None,
        "platelets": None,
        "serum_creatinine": None,
        "serum_sodium": None
    }

    anaemia_match = find_field(text, ['Anaemia', 'Anemia'], r'([A-Za-z]+)')
    if anaemia_match:
        data["anaemia"] = anaemia_match.group(1).strip()

    cpk_match = find_field(text, ['Creatinine Phosphokinase', 'Creatine Phosphokinase', 'Creatinine kinase', 'CK', 'CPK', 'CPK level'], r'([\d,.]+)')
    if cpk_match:
        data["creatinine_phosphokinase"] = float(cpk_match.group(1).replace(',', ''))

    diabetes_match = find_field(text, ['Diabetes', 'Diabetic'], r'([A-Za-z]+)')
    if diabetes_match:
        data["diabetes"] = diabetes_match.group(1).strip()

    ef_match = find_field(text, ['Ejection Fraction', 'EF'], r'(\d+)%?')
    if ef_match:
        data["ejection_fraction"] = int(ef_match.group(1))

    hbp_match = find_field(text, ['High Blood Pressure', 'Hypertension'], r'([A-Za-z]+)')
    if hbp_match:
        data["high_blood_pressure"] = hbp_match.group(1).strip()

    platelets_match = find_field(text, ['Platelets'], r'([\d,]+)')
    if platelets_match:
        data["platelets"] = int(platelets_match.group(1).replace(',', ''))

    serum_creat_match = find_field(text, ['Serum Creatinine', 'Creatinine'], r'([\d.]+)')
    if serum_creat_match:
        data["serum_creatinine"] = float(serum_creat_match.group(1))

    serum_sod_match = find_field(text, ['Serum Sodium', 'Sodium'], r'([\d.]+)')
    if serum_sod_match:
        data["serum_sodium"] = float(serum_sod_match.group(1))

    return data

file = text_extract('example.pdf')