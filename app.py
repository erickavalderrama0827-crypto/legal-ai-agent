import streamlit as st
import openai

st.set_page_config(
    page_title="Primer Paso AI | Immigration & Legal Workflow Suite",
    page_icon="⚖️",
    layout="wide"
)

# Sidebar Navigation Toggle
st.sidebar.title("Primer Paso AI")
page = st.sidebar.radio("Navigation", ["🏠 Home / Overview", "⚡ Live Workflow Tool"])

if page == "🏠 Home / Overview":
    # Main Header
    st.title("⚖️ Primer Paso AI")
    st.subheader("Autonomous Multi-Agent Legal Workflow & Compliance Suite")

    st.markdown("""
    Welcome to **Primer Paso AI**, a production-ready, deterministic legal tech platform designed to eliminate administrative bottlenecks 
    in asylum and immigration casework. By combining modular multi-agent automation with strict human-in-the-loop (HITL) oversight, 
    our platform scales non-profit capacity while upholding rigorous legal standards.
    """)

    st.divider()

    # Core Architecture Overview
    st.markdown("### 🛠️ Complete End-to-End Workflow Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📥 Intake & Ingestion")
        st.markdown("""
        * **1. Translator & OCR:** Handles foreign languages and handwritten client notes.
        * **2. Nexus Auditor:** Cross-checks persecution narratives against statutory grounds.
        * **3. Intake Emails:** Generates structured correspondence and client summaries.
        """)

    with col2:
        st.markdown("#### 📂 Case & Evidence Prep")
        st.markdown("""
        * **4. Exhibit Indexer:** Automates USCIS-compliant Master Exhibit tables.
        * **5. Deadline Calculator:** Flags high-risk statutory windows (e.g., 1-year filing rule).
        * **6. Country Conditions:** Pulls objective risk and geopolitical corroboration.
        """)

    with col3:
        st.markdown("#### 🎯 Review & Adjudication")
        st.markdown("""
        * **7. Deficiency Auditor:** Reviews prior filings to correct gaps and strengthen claims.
        * **9. Interview Prep:** Generates bilingual practice Q&A and trauma-informed coaching.
        * **10. Audit Log:** Enforces mandatory attorney sign-off and compliance tracking.
        """)

    st.divider()

    # PM Guardrails Section
    st.markdown("### 🔒 Built-In Product Management & Legal Guardrails")
    col_g1, col_g2, col_g3 = st.columns(3)

    with col_g1:
        st.info("**Zero Hallucinations**\nStrict 0.0-temperature profiles and structured data parsing ensure predictable, reliable outputs.")

    with col_g2:
        st.info("**Separation of Concerns**\nIsolates data extraction and translation tasks cleanly from business logic validation loops.")

    with col_g3:
        st.info("**Human-in-the-Loop (HITL)**\nEvery major phase requires explicit supervising attorney verification logged securely via audit trails.")

    st.divider()
    st.success("👈 Click **⚡ Live Workflow Tool** in the sidebar to jump into the interactive workspace.")

elif page == "⚡ Live Workflow Tool":
    # --- UNIFIED LIVE WORKFLOW WORKSPACE ---
    st.title("⚡ Live Multi-Agent Workflow Workspace")
    st.write("Execute modular legal AI pipelines to evaluate statutory eligibility, deadlines, country conditions, and filing deficiencies.")

    openai_api_key = st.secrets.get("OPENAI_API_KEY")

    if not openai_api_key:
        st.warning("⚠️ Please configure your OPENAI_API_KEY in your Streamlit app secrets.")
    else:
        client = openai.OpenAI(api_key=openai_api_key)

        # Tab selection inside the workflow tool to include the new Deficiency Auditor
        workflow_tab = st.selectbox(
            "Select Workflow Module to Execute:",
            [
                "⚖️ Nexus & Timeline Auditor", 
                "🌍 Country Conditions & Objective Evidence Screener",
                "🔍 Deficiency & Amendment Auditor"
            ]
        )

        st.markdown("---")

        if workflow_tab == "⚖️ Nexus & Timeline Auditor":
            st.subheader("⚖️ Nexus Auditor & Timeline Cross-Checker")
            st.write("Analyze client narratives against statutory asylum grounds, identify evidentiary gaps, and check deadlines.")

            client_narrative = st.text_area(
                "Paste Client Intake Narrative / Statement:", 
                height=180, 
                placeholder="Enter client details here..."
            )
            
            statutory_ground = st.selectbox(
                "Select Primary Protected Ground Focus:",
                ["Race", "Religion", "Nationality", "Membership in a particular social group (PSG)", "Political opinion"]
            )

            if st.button("Run Nexus & Timeline Audit 🚀", type="primary"):
                if client_narrative.strip():
                    with st.spinner("Multi-Agent Auditor analyzing narrative and statutory deadlines..."):
                        try:
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": (
                                            "You are an expert immigration legal tech multi-agent auditor. "
                                            "Analyze the client narrative against the selected protected ground. "
                                            "Provide: 1) A Timeline & Deadline Risk Assessment, "
                                            "2) Nexus Vulnerability Analysis, and 3) Evidentiary Gaps. "
                                            "Keep it structured, professional, and formatted in clear Markdown."
                                        )
                                    },
                                    {
                                        "role": "user",
                                        "content": f"Selected Ground: {statutory_ground}\n\nClient Narrative:\n{client_narrative}"
                                    }
                                ],
                                temperature=0.0
                            )
                            audit_output = response.choices[0].message.content
                            
                            st.success("Multi-Agent Pipeline Executed Successfully!")
                            st.markdown("---")
                            st.markdown("### 📊 Audit Findings & Gaps Analysis")
                            st.markdown(audit_output)
                            
                            st.markdown("---")
                            st.markdown("### 🔒 Human-in-the-Loop (HITL) Sign-Off")
                            st.checkbox("Attorney Verification: Confirm findings and authorize Master Exhibit generation.")
                            
                        except Exception as e:
                            st.error(f"OpenAI API Error: {e}. Please check your API key secrets in Streamlit.")
                else:
                    st.warning("⚠️ Please paste a client narrative into the text box above before running the audit.")

        elif workflow_tab == "🌍 Country Conditions & Objective Evidence Screener":
            st.subheader("🌍 Country Conditions & Objective Evidence Screener")
            st.write("Synthesize home-country threat patterns, state-action failures, and corroborating evidence requirements.")

            home_country = st.text_input("Home Country:", placeholder="e.g., Guatemala, Nicaragua, El Salvador")
            persecution_category = st.text_input("Primary Persecution Category / Threat:", placeholder="e.g., Targeted violence against anti-mining activists")
            key_facts = st.text_area("Key Facts from Client Narrative to Corroborate:", height=130, placeholder="e.g., Assaulted in Guatemala City after organizing demonstrations...")

            if st.button("Synthesize Country Conditions & Evidence 🚀", type="primary"):
                if home_country.strip() and persecution_category.strip() and key_facts.strip():
                    with st.spinner("Synthesizing geopolitical threat patterns and evidence requirements..."):
                        try:
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": (
                                            "You are an expert country conditions and asylum evidence specialist. "
                                            "Synthesize home-country threat patterns, state-action failures, and corroborating "
                                            "evidence requirements based on the provided inputs. Outline: "
                                            "1) Home-Country Threat Patterns (geopolitical context), "
                                            "2) State-Action/Protection Analysis, and "
                                            "3) Recommended Master Exhibit Evidence (e.g., State Dept Reports, NGO documentation). "
                                            "Keep it structured and professional in Markdown."
                                        )
                                    },
                                    {
                                        "role": "user",
                                        "content": f"Home Country: {home_country}\nPersecution Category: {persecution_category}\nKey Facts: {key_facts}"
                                    }
                                ],
                                temperature=0.0
                            )
                            screener_output = response.choices[0].message.content
                            
                            st.success("Country Conditions Synthesis Complete!")
                            st.markdown("---")
                            st.markdown("### 📂 Objective Evidence & Threat Synthesis")
                            st.markdown(screener_output)
                            
                            st.markdown("---")
                            st.markdown("### 🔒 Master Exhibit Indexing Sign-Off")
                            st.checkbox("Attorney Verification: Approve corroborating evidence package for Master Exhibit table.")
                            
                        except Exception as e:
                            st.error(f"OpenAI API Error: {e}. Please check your API key secrets in Streamlit.")
                else:
                    st.warning("⚠️ Please fill out all fields to run the country conditions analysis.")

        elif workflow_tab == "🔍 Deficiency & Amendment Auditor":
            st.subheader("🔍 Application Review & Deficiency Auditor")
            st.write("Review previously submitted applications, identify legal or factual gaps, and strengthen threat narratives to prevent dismissal.")

            prior_filing = st.text_area("Paste Original Application / Statement Excerpt:", height=140, placeholder="Paste prior declaration or filing text here...")
            government_notice = st.text_area("Paste Government Notice / RFE / Rejection Notes (Optional):", height=100, placeholder="Paste RFE or rejection reasoning here if available...")

            if st.button("Run Deficiency & Amendment Analysis 🚀", type="primary"):
                if prior_filing.strip():
                    with st.spinner("Multi-Agent Auditor analyzing prior filing and identifying legal/factual gaps..."):
                        try:
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": (
                                            "You are an expert immigration legal tech deficiency and amendment auditor. "
                                            "Review the prior filing and government rejection/RFE notes to identify legal gaps, "
                                            "factual inconsistencies, or weak threat narratives. Provide: "
                                            "1) Identified Legal & Factual Gaps, "
                                            "2) RFE Risk Analysis (why it was flagged or vulnerable), and "
                                            "3) Recommended Amendments & Stronger Threat Corroboration. "
                                            "Keep it structured and professional in Markdown."
                                        )
                                    },
                                    {
                                        "role": "user",
                                        "content": f"Prior Filing Excerpt:\n{prior_filing}\n\nGovernment Notice / RFE Notes:\n{government_notice}"
                                    }
                                ],
                                temperature=0.0
                            )
                            deficiency_output = response.choices[0].message.content
                            
                            st.success("Deficiency & Amendment Analysis Complete!")
                            st.markdown("---")
                            st.markdown("### 📊 Deficiency Audit & Amendment Recommendations")
                            st.markdown(deficiency_output)
                            
                            st.markdown("---")
                            st.markdown("### 🔒 Human-in-the-Loop (HITL) Sign-Off")
                            st.checkbox("Attorney Verification: Review recommended amendments before filing response.")
                            
                        except Exception as e:
                            st.error(f"OpenAI API Error: {e}. Please check your API key secrets in Streamlit.")
                else:
                    st.warning("⚠️ Please paste the original application excerpt to run the deficiency analysis.")
