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

# Initialize OpenAI client (it automatically picks up your OPENAI_API_KEY from secrets or environment)
client = OpenAI()

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
                    model="gpt-4o-mini", # or your preferred model
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
                ]
                
                translated_text = response.choices[0].message.content
                
                st.success("Translation Complete:")
                st.write(translated_text)
                
            except Exception as e:
                st.error(f"An error occurred during translation: {e}")
