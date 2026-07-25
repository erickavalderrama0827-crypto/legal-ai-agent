import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Intake Generator", page_icon="✉️", layout="wide")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.subheader("✉️ Automated Intake & Document Checklist Generator")

client_name = st.text_input("Client Full Name:")
case_type = st.selectbox("Case Type:", ["Asylum (I-589)", "Family Petition", "U-Visa / VAWA", "Adjustment of Status"])

client_language = st.selectbox(
    "Preferred Communication Language:",
    [
        "English", 
        "Spanish", 
        "French", 
        "Mandarin (Chinese)", 
        "Arabic", 
        "Portuguese", 
        "Haitian Creole", 
        "Vietnamese", 
        "Russian"
    ]
)

st.markdown("### Select Required Initial Documents:")
col1, col2 = st.columns(2)
with col1:
    req_passport = st.checkbox("Passport / Travel Documents", value=True)
    req_i94 = st.checkbox("I-94 Arrival/Departure Record", value=True)
    req_ID = st.checkbox("National ID / Birth Certificate", value=True)
with col2:
    req_narrative = st.checkbox("Written Personal Statement / Notes", value=True)
    req_medical = st.checkbox("Medical or Police Records (if any)", value=False)
    req_prior_filings = st.checkbox("Prior USCIS Notices / Court Documents", value=False)

if st.button("Generate Client Intake Email"):
    if not client_name.strip():
        st.warning("Please enter the client's name.")
    else:
        with st.spinner("Drafting intake communication..."):
            docs_list = []
            if req_passport: docs_list.append("- Copy of passport (biographic page and all pages with stamps/visas)")
            if req_i94: docs_list.append("- Form I-94 Arrival/Departure record")
            if req_ID: docs_list.append("- Birth certificate or national id card")
            if req_narrative: docs_list.append("- Initial written notes or summary of experiences")
            if req_medical: docs_list.append("- Relevant medical or police reports")
            if req_prior_filings: docs_list.append("- Copies of any past USCIS receipts, notices, or court paperwork")
            
            formatted_docs = "\n".join(docs_list)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a senior immigration paralegal. Write a warm, highly professional, and clear intake email to a prospective client named {client_name} regarding their {case_type} matter. The email must be written entirely in {client_language}. Outline the required documents clearly, explain how to upload them securely, and maintain a reassuring, trauma-informed tone."
                    },
                    {
                        "role": "user",
                        "content": f"Here are the specific documents requested for this client:\n{formatted_docs}"
                    }
                ],
                temperature=0.2
            )
            
            st.success("Intake Email Generated:")
            st.code(response.choices[0].message.content, language="markdown")
