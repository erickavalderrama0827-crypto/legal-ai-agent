import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Exhibit Indexer", page_icon="📂", layout="wide")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.subheader("📂 Master Exhibit Index & Packet Organizer")

st.markdown("Drop or list your compiled case documents to automatically generate a formal USCIS-compliant Exhibit List and Index.")

exhibit_notes = st.text_area(
    "List the documents gathered for this case (e.g., 'Client passport', 'Birth cert', 'Hospital bill from 2024', 'Country report on cartel violence', 'Letter from uncle'):"
)

if st.button("Generate Master Exhibit Index"):
    if not exhibit_notes.strip():
        st.warning("Please enter your gathered case documents.")
    else:
        with st.spinner("Structuring exhibits and building USCIS-compliant index..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a master immigration paralegal expert in USCIS and Executive Office for Immigration Review (EOIR) filing standards. "
                            "Take the user's raw list of documents and organize them into a formal, sequential Master Exhibit Index. "
                            "Group them logically (e.g., Tab A: Identity & Civil Documents, Tab B: Personal Declaration & Evidence, Tab C: Medical/Police Records, Tab D: Country Conditions). "
                            "Output a clean Markdown table with columns: Exhibit Tab, Document Description, and Purpose in Case."
                        )
                    },
                    {
                        "role": "user",
                        "content": exhibit_notes
                    }
                ],
                temperature=0.1
            )
            
            st.success("Master Exhibit Index Created:")
            st.markdown(response.choices[0].message.content)
