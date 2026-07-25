import streamlit as st
import openai
import base64

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
        
        if st.button("Process Document & Translate"):
            with st.spinner("Extracting text and translating..."):
                try:
                    # Encode uploaded image to base64 for OpenAI Vision
                    bytes_data = uploaded_file.getvalue()
                    base64_image = base64.b64encode(bytes_data).decode("utf-8")
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": f"You are an expert legal assistant and translator. Transcribe all visible text (including handwritten notes) from the provided image accurately, and then provide a professional translation into {target_language}."
                            },
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Please extract the text and translate it."},
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                    }
                                ]
                            }
                        ],
                        max_tokens=1500
                    ]
                    
                    st.success("Document processed successfully!")
                    st.markdown("### Extraction & Translation Results")
                    st.markdown(response.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"An error occurred during processing: {e}")
