import streamlit as st
import openai

st.set_page_config(page_title="Nexus Auditor", page_icon="⚖️", layout="wide")

st.title("⚖️ Nexus Auditor & Timeline Cross-Checker")
st.write("Analyze client narratives against statutory asylum grounds, identify evidentiary gaps, and check timelines.")

# Initialize OpenAI client securely from Streamlit secrets
openai_api_key = st.secrets.get("OPENAI_API_KEY")

if not openai_api_key:
    st.warning("Please configure your OPENAI_API_KEY in your Streamlit app secrets.")
else:
    client = openai.OpenAI(api_key=openai_api_key)

    client_narrative = st.text_area("Paste Client Intake Narrative / Statement:", height=200, placeholder="Enter client details here...")
    
    statutory_ground = st.selectbox(
        "Select Primary Protected Ground Focus:",
        ["Race", "Religion", "Nationality", "Membership in a particular social group (PSG)", "Political opinion"]
    )

    if st.button("Run Nexus & Timeline Audit"):
        if client_narrative.strip():
            with st.spinner("Analyzing narrative and cross-checking timeline..."):
                # Placeholder for API call execution
                st.success("Audit complete!")
                st.markdown("### Audit Findings & Gaps")
                st.info("Analysis results will display here.")
        else:
            st.warning("Please enter a client narrative to run the audit.")
