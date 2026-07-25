import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client right at the top
client = OpenAI()
import os
import streamlit as st
from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser

class ExtractedClientData(BaseModel):
    full_name: str = Field(description="The full legal name of the applicant.")
    birth_date: str = Field(description="Date of birth in YYYY-MM-DD format.")
    country_of_origin: str = Field(description="The country the applicant is fleeing.")
    entry_date_us: str = Field(description="The date the client entered the US (YYYY-MM-DD).")
    harm_narrative_summary: str = Field(description="A summary of the specific harm feared or experienced.")

class DiscrepancyReport(BaseModel):
    issue_found: bool = Field(description="True if a contradiction or missing field is detected.")
    severity: str = Field(description="HIGH or MEDIUM severity warning.")
    audit_notes: List[str] = Field(description="Detailed explanation of the conflicts found.")

def run_legal_workflow(unstructured_client_input: str, api_key: str):
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0, openai_api_key=api_key)
    parser_1 = PydanticOutputParser(pydantic_object=ExtractedClientData)
    prompt_1 = ChatPromptTemplate.from_template(
        "You are a Legal Intake AI Specialist. Extract structured biographical data from this testimony:\n"
        "'{input}'\n\n{format_instructions}"
    )
    prompt_1_formatted = prompt_1.format_messages(input=unstructured_client_input, format_instructions=parser_1.get_format_instructions())
    response_1 = llm.invoke(prompt_1_formatted)
    extracted_data = parser_1.parse(response_1.content)
    
    parser_2 = PydanticOutputParser(pydantic_object=DiscrepancyReport)
    prompt_2 = ChatPromptTemplate.from_template(
        "You are a Senior Immigration Attorney. Review the extracted metadata and flag any timeline risks, mismatches, or violations of the 1-year US filing deadline:\n"
        "'{metadata}'\n\n{format_instructions}"
    )
    prompt_2_formatted = prompt_2.format_messages(metadata=str(extracted_data), format_instructions=parser_2.get_format_instructions())
    response_2 = llm.invoke(prompt_2_formatted)
    audit_report = parser_2.parse(response_2.content)
    return extracted_data, audit_report

st.set_page_config(page_title="Legal AI Intake Dashboard", layout="wide")
st.title("⚖️ Autonomous Asylum Intake & Consistency Auditor")
st.caption("AI Product Management Portfolio Concept")
st.markdown("---")

st.sidebar.header("Developer Configurations")
user_api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.environ.get("OPENAI_API_KEY", ""))

st.subheader("📋 Step 1: Input Unstructured Testimony")
default_intake = (
    "Me llamo Carlos Mendoza. I arrived in the US around August 15, 2024, after crossing near El Paso. "
    "I was born on May 12, 1994. I cannot go back to Venezuela because local gangs threatened to burn my "
    "shop down in Caracas if I didn't pay protection money. They attacked my brother in July of 2025 because of this."
)
client_text = st.text_area("Paste raw intake text:", value=default_intake, height=150)

if st.button("Execute Multi-Agent Legal Audit", type="primary"):
    if not user_api_key:
        st.error("Please enter a valid OpenAI API Key in the left sidebar to proceed.")
    else:
        with st.spinner("Processing..."):
            try:
                data, audit = run_legal_workflow(client_text, user_api_key)
                st.markdown("### 📊 Step 2: Multi-Agent Analysis Output")
                col1, col2 = st.columns(2)
                with col1:
                    st.info("📂 Agent 1: Structured Biographical Metadata Extraction")
                    st.text_input("Full Legal Name", value=data.full_name, disabled=True)
                    st.text_input("Date of Birth", value=data.birth_date, disabled=True)
                    st.text_input("Country of Origin", value=data.country_of_origin, disabled=True)
                    st.text_input("US Entry Date", value=data.entry_date_us, disabled=True)
                    st.text_area("Narrative Summary of Harm", value=data.harm_narrative_summary, height=80, disabled=True)
                with col2:
                    st.warning("🛡️ Agent 2: Legal Risk & Compliance Audit Report")
                    st.metric(label="Risk Mismatches Found", value=str(audit.issue_found))
                    st.error(f"Alert Status: {audit.severity} SEVERITY RISK")
                    for note in audit.audit_notes:
                        st.markdown(f"- {note}")
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
                import streamlit as st
from openai import OpenAI
st.subheader("🌐 Multi-Lingual Intake Translator")

# Text box for raw client notes (e.g., Spanish, French, etc.)
raw_notes = st.text_area("Paste foreign-language intake notes here:")

target_language = st.selectbox(
    "Translate into:",
    ["English", "Spanish"]
)

if st.button("Translate and Structure Notes"):
    if not raw_notes.strip():
        st.warning("Please enter some text to translate first.")
    else:
        with st.spinner("Translating and analyzing..."):
            try:
                # Prompt the model to act as a legal translator and analyst
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system", 
                            "content": f"You are an expert legal assistant. Translate the following intake notes accurately into {target_language}. Maintain professional legal phrasing and format any key dates or entities clearly."
                        },
                        {
                            "role": "user", 
                            "content": raw_notes
                        }
                    ],
                    temperature=0.1
                )
                
                translated_text = response.choices[0].message.content
                
                st.success("Translation Complete:")
                st.write(translated_text)
                
            except Exception as e:
                st.error(f"An error occurred during translation: {e}")
                st.subheader("📄 Handwritten Notes & Image Ingestion")
                st.subheader("📄 Handwritten Notes & Image Ingestion")

# File uploader that accepts common image formats
uploaded_image = st.file_uploader(
    "Upload a photo or scanned copy of handwritten client notes:", 
    type=["png", "jpg", "jpeg"]
)

if uploaded_image is not None:
    # Display the uploaded image in the app
    st.image(uploaded_image, caption="Uploaded Intake Document", use_column_width=True)
    
    if st.button("Extract and Process Handwritten Notes"):
        with st.spinner("Reading handwriting and structuring data..."):
            try:
                # Read the image bytes and encode to base64 for the vision model
                import base64
                image_bytes = uploaded_image.getvalue()
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert legal assistant. Carefully read the handwriting in this intake document. Transcribe it accurately, fix any obvious spelling errors, and format it into a structured summary with key headings (e.g., Client Information, Dates of Entry, Reasons for Fear/Persecution)."
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": "Please transcribe and structure the handwritten notes from this image:"
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
                
                st.success("Extraction Complete:")
                st.markdown(extracted_text)
                
            except Exception as e:
                st.error(f"An error occurred while reading the image: {e}")
                st.divider()
st.subheader("⚖️ Advanced Asylum Application Modules")

# Choose which module to run
module_choice = st.selectbox(
    "Select Workflow Tool:",
    ["Select a tool...", "Timeline & Gap Analyzer", "Address History Formatter", "1-Year Deadline Screener"]
)

if module_choice == "Timeline & Gap Analyzer":
    st.markdown("### 📅 Timeline & Inconsistency Check")
    timeline_input = st.text_area("Paste client statements, notes, or mixed date records:")
    
    if st.button("Generate Chronological Timeline"):
        if timeline_input.strip():
            with st.spinner("Analyzing dates and finding gaps..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a meticulous legal analyst. Extract all dates and events from the text, build a clean chronological timeline, and explicitly flag any suspicious gaps, overlaps, or inconsistencies that could hurt an asylum applicant's credibility."},
                        {"role": "user", "content": timeline_input}
                    ],
                    temperature=0.1
                )
                st.markdown(response.choices[0].message.content)

elif module_choice == "Address History Formatter":
    st.markdown("### 🏠 5-Year Address History Builder (Form I-589)")
    address_input = st.text_area("Describe the client's past living locations and rough timeframes:")
    
    if st.button("Format Address History"):
        if address_input.strip():
            with st.spinner("Structuring address record..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an immigration form assistant. Convert the user's rough narrative of living places into a clean, structured table format showing Street Address, City, Country, From (MM/YY), and To (MM/YY) for the past 5 years."},
                        {"role": "user", "content": address_input}
                    ],
                    temperature=0.1
                )
                st.markdown(response.choices[0].message.content)

elif module_choice == "1-Year Deadline Screener":
    st.markdown("### ⏰ Filing Deadline & Exception Screener")
    entry_date = st.date_input("Date of Last Arrival in the U.S.:")
    narrative_context = st.text_area("Any notes regarding circumstances if past the 1-year mark:")
    
    if st.button("Check Deadline Status"):
        with st.spinner("Calculating timeline window..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an asylum law compliance clerk. Calculate whether the 1-year filing deadline has passed based on the given arrival date. Outline the legal standard for exceptions (changed or extraordinary circumstances) if applicable."},
                    {"role": "user", "content": f"Last arrival date: {entry_date}. Additional context: {narrative_context}"}
                ],
                temperature=0.1
            )
            st.markdown(response.choices[0].message.content)

