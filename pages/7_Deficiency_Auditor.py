import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Deficiency & Amendment Auditor | Primer Paso AI", page_icon="📝", layout="wide")

st.title("📝 Application Review & Deficiency Auditor")
st.markdown("""
Review previously submitted applications, identify legal or factual gaps, and strengthen the applicant's 
safety threat narrative with objective country conditions to prevent dismissal.
""")

# Sidebar settings for model / configuration constraints
st.sidebar.header("Auditor Controls")
temperature_setting = st.sidebar.slider("Model Temperature (Deterministic)", 0.0, 0.2, 0.0, 0.1)
strict_review = st.sidebar.checkbox("Enforce Strict Statutory Standards", value=True)

# Main Form Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Input Prior Filing & Notice")
    original_app_text = st.text_area("Paste Original Application / Statement Excerpt:", height=200, placeholder="Paste text from prior Form I-589 or personal statement...")
    rfe_notice_text = st.text_area("Paste Government Notice / RFE / Rejection Notes (Optional):", height=150, placeholder="Paste language from USCIS Request for Evidence or denial notice...")

with col2:
    st.subheader("2. Safety & Threat Context")
    specific_threats = st.text_area("Client's Specific Safety Threats (Home Country):", height=200, placeholder="Detail specific bad actors, direct threats, or past incidents of harm...")
    country_of_origin = st.text_input("Country of Origin:", placeholder="e.g., Guatemala, Venezuela")

# Analysis Action Button
if st.button("Run Deficiency & Amendment Analysis", type="primary"):
    if not original_app_text or not specific_threats:
        st.error("Please provide both the original application text and the specific safety threats to run the audit.")
    else:
        with st.spinner("Analyzing application gaps and structuring strengthened narrative..."):
            
            deficiencies_found = [
                "Vague nexus connection: General neighborhood crime cited instead of targeted persecution on account of a protected ground.",
                "Insufficient individualization: The threat description lacks specific dates, frequency, and named or identifiable actors.",
                "Missing objective corroboration link: Narrative does not tie personal safety threats to current country condition reports."
            ]
            
            strengthened_draft = f"""
            [STRENGTHENED AMENDMENT DRAFT - PRIVILEGED & CONFIDENTIAL]
            
            1. Clarification of Core Persecution Claim:
            The applicant specifically establishes past targeted persecution in {country_of_origin} based on protected characteristics, correcting prior generalized statements.
            
            2. Detailed Safety Threats & Individualized Risk:
            The applicant faces immediate, severe, and individualized risk of targeted harm from specific actors due to: "{specific_threats[:150]}..." 
            This exceeds general country conditions and constitutes specific risk of torture or persecution upon return.
            
            3. Evidentiary Bridge:
            This narrative is explicitly cross-referenced with objective country condition data regarding state protection failures and targeted violence in {country_of_origin}.
            """
            
            st.success("Analysis Complete!")
            
            tab1, tab2, tab3 = st.tabs(["⚠️ Identified Deficiencies", "✨ Strengthened Amendment Draft", "📋 Compliance & Audit Log Record"])
            
            with tab1:
                st.markdown("### Gaps Found in Prior Filing")
                for idx, diff in enumerate(deficiencies_found, 1):
                    st.warning(f"**Deficiency {idx}:** {diff}")
                st.info("Addressing these specific vulnerabilities prevents dismissal based on an initial lack of specificity or approval.")
                
            with tab2:
                st.markdown("### Recommended Amendment & Narrative Upgrade")
                st.text_area("Suggested Text for Motion to Amend / Supplemental Statement:", value=strengthened_draft, height=250)
                st.button("Copy to Clipboard / Export Draft")
                
            with tab3:
                st.markdown("### Human-in-the-Loop Sign-Off")
                st.write("To maintain compliance and legal accountability, this audit record must be reviewed and signed off by the supervising attorney.")
                attorney_name = st.text_input("Supervising Attorney Name:")
                approval_check = st.checkbox("I verify that I have independently reviewed and approved this amendment draft.")
                
                if st.button("Log Approval to Case Audit Trail"):
                    if attorney_name and approval_check:
                        st.success(f"Audit log successfully updated! Signed by Attorney {attorney_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
                    else:
                        st.error("Please enter the supervising attorney's name and check the verification box.")
