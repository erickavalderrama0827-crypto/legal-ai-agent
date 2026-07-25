import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Translator & OCR", page_icon="🌐", layout="wide")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.subheader("📄 Multilingual Handwritten Notes & Image Ingestion")

handwriting_lang = st.selectbox(
    "Handwritten Document Language:",
    ["Spanish", "French", "English", "Arabic", "Mandarin (Chinese)", "Portuguese", "Haitian Creole", "Other"],
    key="hw_lang"
)

uploaded_image = st.file_uploader(
    "Upload a photo or scanned copy of handwritten client notes:", 
    type=["png", "jpg", "jpeg"],
    key="hw_uploader"
)

if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded Intake Document", use_container_width=True)
    
    if st.button("Extract and Translate Handwritten Notes"):
        with st.spinner("Reading handwriting and structuring data..."):
            try:
                import base64
                image_bytes = uploaded_image.getvalue()
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are an expert legal assistant and translator. Carefully read the handwritten {handwriting_lang} text in this intake document. Transcribe it accurately, translate it into professional English legal phrasing if necessary, and format it into a structured summary with key headings (e.g., Client Information, Dates of Entry, Reasons for Fear/Persecution)."
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": f"Please transcribe and structure the handwritten {handwriting_lang} notes from this image:"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=1000,
                    temperature=0.1
                )
                
                extracted_text = response.choices[0].message.content
                st.success("Extraction & Translation Complete:")
                st.markdown(extracted_text)
                
            except Exception as e:
                st.error(f"An error occurred while reading the image: {e}")
