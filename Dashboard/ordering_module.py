import pandas as pd
import pdfplumber
import io
from drug_classifier import classify_drug

def extract_pdf_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def run_ordering_system(invoice_pdf, daily_log, price_threshold):

    invoice_text = extract_pdf_text(invoice_pdf)

    df = pd.read_csv(daily_log)
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

    df["Drug Type"] = df["Drug Name"].apply(classify_drug)

    filtered = df[df["Total"] >= price_threshold]

    # Prefer generics first
    filtered = filtered.sort_values(
        by=["Drug Type", "Total"],
        ascending=[True, False]
    )

    return filtered


def convert_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()
