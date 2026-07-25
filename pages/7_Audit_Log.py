import streamlit as st
from datetime import date

st.set_page_config(page_title="Case Audit & Compliance Log", page_icon="📝", layout="wide")

st.title("📝 Case Audit & Compliance Sign-Off")
st.write("Generate a formal verification record confirming human-in-the-loop review for AI-assisted case components.")

# Intake verification form
with st.form("audit_form"):
    col1, col2 = st.columns(2)
    with col1:
        case_identifier = st.text_input("Case / Client File ID (e.g., A-Number or Initials):", placeholder="Client-001")
        attorney_name = st.text_input("Supervising Attorney / Advocate Name:")
    with col2:
        review_date = st.date_input("Review Date:", value=date.today())
        modules_utilized = st.multiselect(
            "Primer Paso AI Modules Utilized in This Case:",
            [
                "1. Multi-Lingual Translator & OCR",
                "2. Nexus Auditor & Timeline Cross-Checker",
                "3. Intake Email Generator",
                "4. Master Exhibit Indexer",
                "5. 1-Year Deadline Screener",
                "6. Country Conditions Screener"
            ]
        )

    st.divider()
    
    st.markdown("#### Mandatory Professional Verification Statements")
    check_1 = st.checkbox("I confirm that I have independently reviewed, verified, and edited all AI-generated drafts, translations, and timelines for legal accuracy.")
    check_2 = st.checkbox("I confirm that no sensitive client PII has been stored or retained by third-party model training pipelines in compliance with privacy standards.")
    check_3 = st.checkbox("I accept full professional responsibility for the final submissions and communications generated using this software.")

    submitted = st.form_submit_button("Generate Signed Audit Record")

    if submitted:
        if case_identifier.strip() and attorney_name.strip() and (check_1 and check_2 and check_3):
            st.success("Audit record successfully validated and logged!")
            st.divider()
            
            # Display formatted record
            st.markdown(f"### 🛡️ Official Compliance Record: {case_identifier}")
            st.markdown(f"**Supervising Professional:** {attorney_name}")
            st.markdown(f"**Date of Verification:** {review_date.strftime('%B %d, %Y')}")
            st.markdown(f"**Modules Applied:** {', *'.join(modules_utilized)}")
            st.markdown("---")
            st.info(
                "**Attestation Status:** APPROVED. All human-in-the-loop verification checkpoints "
                "have been satisfied. This record is cleared for inclusion in the internal compliance file."
            )
        else:
            st.error("Please fill in all required text fields and check all three professional verification boxes to generate the record.")
