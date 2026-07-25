import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Nexus Auditor", page_icon="⚖️", layout="wide")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.subheader("⚖️ Asylum Legal Nexus & Risk Scrutiny Analyzer")

client_story_input = st.text_area(
    "Paste the client's personal statement or intake narrative for legal risk evaluation:"
)

if st.button("Run Legal Nexus & Credibility Audit"):
    if not client_story_input.strip():
        st.warning("Please paste a narrative to analyze.")
    else:
        with st.spinner("Analyzing text against statutory asylum requirements..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a strict, senior immigration attorney specializing in asylum law. "
                            "Analyze the provided client statement for legal viability. "
                            "Structure your response into 3 clear sections:\n"
                            "1. **Protected Ground Nexus Audit:** Evaluate whether the text successfully connects the harm "
                            "to one of the 5 statutory grounds (Race, Religion, Nationality, Political Opinion, Particular Social Group) "
                            "or if it sounds like generalized criminal violence/extortion that risks denial.\n"
                            "2. **Evidentiary & Detail Gaps:** Point out missing specific dates, locations, or actors that an adjudicator "
                            "or asylum officer will flag.\n"
                            "3. **Recommended Attorney Fixes:** Provide actionable advice on how to legally reframe the narrative."
                        )
                    },
                    {
                        "role": "user",
                        "content": client_story_input
                    }
                ],
                temperature=0.2
            )
            
            st.success("Legal Scrutiny Report Generated:")
            st.markdown(response.choices[0].message.content)
