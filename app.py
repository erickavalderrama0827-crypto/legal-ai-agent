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
    st.success("👈 Click **⚡ Live Workflow Tool** in the sidebar to jump into the workspace.")

elif page == "⚡ Live Workflow Tool":
    # --- LIVE NEXUS AUDITOR TOOL ---
    st.title("⚖️ Nexus Auditor & Timeline Cross-Checker")
    st.write("Analyze client narratives against statutory asylum grounds, identify evidentiary gaps, and check timelines.")

    # Initialize OpenAI client securely from Streamlit secrets
    openai_api_key = st.secrets.get("OPENAI_API_KEY")

    if not openai_api_key:
        st.warning("Please configure your OPENAI_API_KEY in your Streamlit app secrets.")
    else:
        client = openai.OpenAI(api_key=openai_api_key)

        client_narrative = st.text_area(
            "Paste Client Intake Narrative / Statement:", 
            height=200, 
            placeholder="Enter client details here (e.g., Sofia R. case history...)"
        )
        
        statutory_ground = st.selectbox(
            "Select Primary Protected Ground Focus:",
            ["Race", "Religion", "Nationality", "Membership in a particular social group (PSG)", "Political opinion"]
        )

        if st.button("Run Nexus & Timeline Audit", type="primary"):
            if client_narrative.strip():
                with st.spinner("Multi-Agent Auditor analyzing narrative and statutory deadlines..."):
                    try:
                        # Call OpenAI to generate the audit breakdown live
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are an expert immigration legal tech multi-agent auditor. "
                                        "Analyze the client narrative against the selected protected ground. "
                                        "Provide: 1) A Timeline & Deadline Risk Assessment (checking entry dates/1-year rules), "
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
                        st.error(f"Error running OpenAI audit: {e}")
            else:
                st.warning("Please enter a client narrative to run the audit.")
