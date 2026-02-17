import streamlit as st
import pandas as pd
import high_reimbursement_module as hr
import ordering_module as om

st.set_page_config(page_title="Pharmacy Intelligence Platform", layout="wide")

st.title("💊 Pharmacy Intelligence & Audit Platform")

project_option = st.sidebar.selectbox(
    "Select Project",
    ["High Reimbursement Audit", "Ordering Optimization"]
)

# =========================================================
# PROJECT 1: HIGH REIMBURSEMENT
# =========================================================

if project_option == "High Reimbursement Audit":

    st.header("High Reimbursement Generic Audit")

    uploaded_file = st.file_uploader(
        "Upload Daily Log CSV",
        type=["csv"],
        key="high_reim"
    )

    min_reim = st.number_input("Minimum Total Reimbursement", value=5000)
    high_avg = st.number_input("High Avg Reimbursement Per Claim", value=500)
    very_high_total = st.number_input("Very High Total Spend", value=50000)

    if uploaded_file:

        result_df = hr.run_high_reimbursement(
            uploaded_file,
            min_reim,
            high_avg,
            very_high_total
        )

        st.success("Audit Completed Successfully")

        st.dataframe(result_df)

        # Download button
        st.download_button(
            label="Download Excel Report",
            data=hr.convert_to_excel(result_df),
            file_name="high_reimbursement_audit.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# =========================================================
# PROJECT 2: ORDERING OPTIMIZATION
# =========================================================

if project_option == "Ordering Optimization":

    st.header("Ordering Optimization System")

    invoice_pdf = st.file_uploader(
        "Upload Invoice PDF (Plain Text)",
        type=["pdf"],
        key="invoice"
    )

    daily_log = st.file_uploader(
        "Upload Daily Log CSV",
        type=["csv"],
        key="daily_log"
    )

    price_threshold = st.number_input(
        "Minimum Price Threshold",
        value=100
    )

    if invoice_pdf and daily_log:

        result_df = om.run_ordering_system(
            invoice_pdf,
            daily_log,
            price_threshold
        )

        st.success("Ordering Recommendation Generated")

        st.dataframe(result_df)

        st.download_button(
            label="Download Ordering Excel",
            data=om.convert_to_excel(result_df),
            file_name="ordering_recommendation.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
