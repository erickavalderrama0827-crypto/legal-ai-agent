import streamlit as st
import openai

st.set_page_config(page_title="Exhibit Index", page_icon="📑", layout="wide")

st.title("📑 Exhibit Index & Document Organizer")
st.write("Organize, index, and generate structured exhibit lists for your legal cases seamlessly.")

# Initialize OpenAI client securely from Streamlit secrets
openai_api_key = st.secrets.get("OPENAI_API_KEY")

if not openai_api_key:
    st.warning("Please configure your OPENAI_API_KEY in your Streamlit app secrets.")
else:
    client = openai.OpenAI(api_key=openai_api_key)

    exhibit_notes = st.text_area("List your compiled case documents and descriptions:", height=180, placeholder="E.g., Birth certificate from El Salvador, Employment letter from 2022, Medical records...")

    if st.button("Generate Master Exhibit Index"):
        if exhibit_notes.strip():
            with st.spinner("Formatting exhibit index..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert legal assistant. Organize the provided document list into a formal, USCIS-compliant Master Exhibit Index formatted neatly as a Markdown table with columns for Exhibit Letter/Number, Description, and Page Count."
                        },
                        {"role": "user", "content": exhibit_notes}
                    ],
                    temperature=0.1
                )
                st.success("Exhibit Index generated successfully!")
                st.markdown("### Master Exhibit Index")
                st.markdown(response.choices[0].message.content)
        else:
            st.warning("Please enter your document list before generating the index.")
