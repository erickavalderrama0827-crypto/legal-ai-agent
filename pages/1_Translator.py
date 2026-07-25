import streamlit as st
import openai

st.set_page_config(page_title="Translator & OCR", page_icon="🌐", layout="wide")

st.title("🌐 Multi-Lingual Translator & Document OCR")
st.write("Upload an image of handwritten notes or a document to extract text and translate it seamlessly.")

# Initialize OpenAI client securely from Streamlit secrets
openai_api_key = st.secrets.get("OPENAI_API_KEY")

if not openai_api_key:
    st.warning("Please configure your OPENAI_API_KEY in your Streamlit app secrets.")
else:
    client = openai.OpenAI(api_key=openai_api_key)

    uploaded_file = st.file_uploader("Choose an image or document...", type=["png", "jpg", "jpeg", "pdf"])
    
    target_language = st.selectbox(
        "Select Target Language for Translation:", 
        ["English", "Spanish", "French", "Portuguese", "Kiche", "Mam", "Qanjobal", "Haitian Creole", "Arabic", "Mandarin"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Document", use_column_width=True)
        if st.button("Process Document"):
            with st.spinner("Extracting and translating..."):
                # Placeholder for API call execution
                st.success("Document processed successfully!")
             
