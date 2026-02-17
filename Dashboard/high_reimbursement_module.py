import pandas as pd
import io
from drug_classifier import classify_drug

def run_high_reimbursement(file, min_reim, high_avg, very_high):

    df = pd.read_csv(file)
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
    df = df.dropna(subset=["Total"])

    df["Drug Type"] = df["Drug Name"].apply(classify_drug)

    summary = (
        df.groupby(["Plan", "NDC", "Drug Name", "Drug Type"], as_index=False)
        .agg(
            Total_Reimbursement=("Total", "sum"),
            Claim_Count=("NDC", "count")
        )
    )

    summary["Avg_Reimbursement_Per_Claim"] = (
        summary["Total_Reimbursement"] / summary["Claim_Count"]
    )

    generic_only = summary[
        (summary["Drug Type"] == "Generic") &
        (summary["Total_Reimbursement"] >= min_reim)
    ].copy()

    def audit_flag(row):
        if row["Avg_Reimbursement_Per_Claim"] >= high_avg:
            return "High Avg Cost Generic"
        if row["Total_Reimbursement"] >= very_high:
            return "Very High Total Spend Generic"
        return "OK"

    generic_only["Audit_Flag"] = generic_only.apply(audit_flag, axis=1)

    return generic_only.sort_values("Total_Reimbursement", ascending=False)


def convert_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()
