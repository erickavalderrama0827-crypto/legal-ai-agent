import streamlit as st
import openai

st.set_page_config(page_title="Country Conditions Screener", page_icon="🌍", layout="wide")

st.title("🌍 Country Conditions & Objective Evidence Screener")
st.write("Synthesize home-country threat patterns, state-action failures, and corroborating evidence requirements.")

# Initialize OpenAI client securely from Streamlit secrets
openai_api_key = st.secrets.get("OPENAI_API_KEY")

if not openai_api_key:
    st.warning("Please configure your OPENAI_API_KEY in your Streamlit app secrets.")
else:
    client = openai.OpenAI(api_key=openai_api_key)

    col1, col2 = st.columns(2)

    with col1:
        home_country = st.text_input("Home Country:", placeholder="E.g., Guatemala, Venezuela, El Salvador...")
    with col2:
        threat_type = st.selectbox(
            "Primary Persecution Category / Threat:",
            [
                "Gang / Cartel Extortion & Violence",
                "Political Targeting & Government Repression",
                "Gender-Based Violence / Domestic Persecution",
                "Religious or Ethnic Minorities",
                "LGBTQ+ Targeted Harassment",
                "Other / Mixed Motivations"
            ]
        )

    specific_facts = st.text_area(
        "Key Facts from Client Narrative to Corroborate:",
        height=150,
        placeholder="E.g., Targeted by Barrio 18 in zone 4 of Guatemala City for refusing extortion payments between 2023 and 2025; local police refused to file report..."
    )

    if st.button("Generate Country Conditions Research Outline"):
        if home_country.strip() and specific_facts.strip():
            with st.spinner("Analyzing threat patterns and drafting objective evidence roadmap..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an expert asylum attorney and country conditions researcher. "
                                "Provide a structured objective evidence brief based on the user's home country and threat details. "
                                "Include: 1) Key systemic risk patterns documented in human rights reports, "
                                "2) State-action or police protection failure analysis (to satisfy the inability/unwillingness requirement), "
                                "3) Specific corroborating evidence sources to source (e.g., State Department human rights reports, UNHCR reports, local independent media), and "
                                "4) Specific guidance on internal relocation feasibility."
                            )
                        },
                        {"role": "user", "content": f"Country: {home_country}\nThreat Type: {threat_type}\nClient Narrative Details: {specific_facts}"}
                    ],
                    temperature=0.1
                )
                st.success("Country conditions research outline generated!")
                st.markdown("### Objective Evidence & Conditions Roadmap")
                st.markdown(response.choices[0].message.content)
        else:
            st.warning("Please enter both the home country and the client's narrative details to generate the outline.")
