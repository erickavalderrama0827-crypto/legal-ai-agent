import streamlit as st

st.set_page_config(
    page_title="Primer Paso AI",
    page_icon="⚖️",
    layout="wide"
)

# Main Header
st.title("⚖️ Primer Paso AI Suite")
st.markdown("### Professional Legal Tech Workflow & Intake Automation")
st.write(
    "Welcome to your centralized hub for immigration case management. "
    "Select a tool from the sidebar menu to begin, or use the quick links below."
)

st.divider()

# Dashboard Overview Cards / Quick Links
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🌐 Translator & OCR")
    st.write("Extract text from handwritten notes and documents, with support for multiple indigenous and international languages.")
    
    st.markdown("#### ⚖️ Nexus Auditor")
    st.write("Analyze client narratives against statutory asylum grounds, identify evidentiary gaps, and check timelines.")

with col2:
    st.markdown("#### ✉️ Intake Emails")
    st.write("Draft professional, multi-lingual client follow-ups, document requests, and appointment notices.")
    
    st.markdown("#### 📑 Exhibit Indexer")
    st.write("Organize case files into structured, USCIS-compliant Master Exhibit indexes effortlessly.")

st.divider()
st.info("💡 **Tip:** Use the sidebar navigation on the left to jump directly between any of your active workflow modules.")
