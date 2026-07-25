import streamlit as st
import openai

st.set_page_config(page_title="Intake Emails", page_icon="✉️", layout="wide")

st.title("✉️ Automated Intake Email Generator")
st.write("Generate professional, multi-lingual follow-up emails and information requests for clients.")

# Initialize OpenAI client securely from Streamlit secrets
openai_api_key = st.secrets.get("OPENAI_API_KEY")

if not openai_api_key:
    st.warning("Please configure your OPENAI_API_KEY in your Streamlit app secrets.")
else:
    client = openai.OpenAI(api_key=openai_api_key)

    col1, col2 = st.columns(2)
    
    with col1:
        client_name = st.text_input("Client Name:")
        preferred_language = st.selectbox(
            "Preferred Language:", 
            ["English", "Spanish", "French", "Portuguese", "Kiche", "Mam", "Qanjobal", "Haitian Creole", "Arabic", "Mandarin"]
        )
    
    with col2:
        email_purpose = st.selectbox(
            "Email Purpose:",
            [
                "Missing Evidence / Document Request",
                "Consultation Follow-up & Next Steps",
                "Timeline Clarification Request",
                "Appointment Reminder"
            ]
        )

    additional_notes = st.text_area("Specific Details to Include:", height=150, placeholder="Mention specific documents needed (e.g., birth certificate, police report)...")

    if st.button("Generate Intake Email"):
        if client_name.strip():
            with st.spinner("Drafting professional email..."):
                # Placeholder for API call execution
                st.success("Email generated successfully!")
                st.markdown("### Drafted Email")
                st.info(f"To: {client_name}\nLanguage: {preferred_language}\n\n[Email content preview will appear here.]")
        else:
            st.warning("Please enter the client's name to generate the email.")
