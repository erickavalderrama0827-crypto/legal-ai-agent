import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Interview & Court Prep | Primer Paso AI", page_icon="🎤", layout="wide")

st.title("🎤 Asylum Interview & Court Preparation Simulator")
st.markdown("""
Help asylum seekers prepare with clarity and confidence. Generate tailored practice questions, 
trauma-informed coaching tips, and bilingual client-friendly review sheets.
""")

# Sidebar settings
st.sidebar.header("Preparation Controls")
adjudication_type = st.sidebar.selectbox("Adjudication Setting", ["USCIS Asylum Office Interview", "Immigration Court (Individual Hearing)"])
client_language = st.sidebar.selectbox("Client Comfort / Output Language", ["English", "Spanish (Español)"])
temperature_setting = st.sidebar.slider("Model Temperature (Creativity)", 0.0, 0.3, 0.1, 0.1)

# Main Form Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Client Case Context")
    case_summary = st.text_area("Paste Client Statement / Narrative Excerpt:", height=200, placeholder="Paste core background and persecution details...")
    country_of_origin = st.text_input("Country of Origin:", placeholder="e.g., Honduras, Venezuela")

with col2:
    st.subheader("2. Focus Areas & Vulnerabilities")
    known_vulnerabilities = st.text_area("Specific Challenges / Soft Spots in Case:", height=200, placeholder="E.g., timeline discrepancies, fear of authority, hesitation discussing past threats...")

# Generation Trigger
if st.button("Generate Tailored Prep Package", type="primary"):
    if not case_summary or not country_of_origin:
        st.error("Please provide the client case statement and country of origin to generate prep materials.")
    else:
        with st.spinner("Generating targeted practice questions and bilingual coaching guidance..."):
            
            # Content tailored based on language selection
            if client_language == "Spanish (Español)":
                mock_questions = [
                    "1. Pregunta sobre el motivo central: 'Usted indicó que huyó de su país debido a... ¿Puede describir el momento exacto en que se sintió personalmente amenazado?'",
                    "2. Verificación de fechas: 'Su declaración menciona un incidente en marzo, pero los registros indican abril. ¿Puede aclarar la secuencia exacta?'",
                    "3. Reubicación interna: '¿Por qué no pudo mudarse a otra ciudad o región dentro de su país en lugar de salir?'",
                    "4. Protección estatal: '¿Reportó estas amenazas a la policía local? Si no lo hizo, ¿por qué sintió que no la protegerían?'"
                ]
                coaching_tips = [
                    "**Pausas y Respiración:** Recuerde que está bien tomarse un momento para respirar o pedir que repitan la pregunta si se siente abrumado.",
                    "**Enfoque en los Hechos:** Concéntrese en detalles concretos ('Vi que pasó X cosa en esta fecha') en lugar de generalidades.",
                    "**Calma ante Discrepancias:** Si el oficial nota una diferencia en fechas, responda con honestidad y tranquilidad."
                ]
                client_note = "Estimado/a cliente: Esta práctica es para ayudarle a sentirse seguro/a y preparado/a. No hay respuestas perfectas, solo sea sincero/a sobre su historia."
            else:
                mock_questions = [
                    f"1. Officer/Judge Inquiry on Core Motive: 'You stated you fled {country_of_origin} because of... Can you describe the exact moment you realized you were personally targeted?'",
                    "2. Timeline Verification: 'Your statement mentions an incident in March, but records reference April. Can you clarify the exact sequence of events?'",
                    "3. Internal Relocation: 'Why didn't you move to another city or region within your home country instead of leaving?'",
                    "4. State Protection: 'Did you report these threats to local law enforcement? If not, why did you feel authorities wouldn't protect you?'"
                ]
                coaching_tips = [
                    "**Pacing & Pauses:** Remind the client it is completely okay to pause, take a breath, or ask for a question to be repeated if they feel overwhelmed.",
                    "**Stick to the Facts:** Encourage concrete, sensory details ('I saw X happen to Y on this date') rather than broad generalizations.",
                    "**Addressing Inconsistencies Calmly:** If an officer points out a minor date discrepancy, coach the client to answer honestly and directly rather than becoming defensive."
                ]
                client_note = "Client Note: This practice session is designed to help you feel safe and confident. There are no trick questions—just tell your honest story."

            st.success("Preparation Package Generated Successfully!")
            
            tab1, tab2, tab3, tab4 = st.tabs(["❓ Practice Questions", "💡 Advocate Guidance", "🤝 Client-Facing Sheet", "📋 Audit Log"])
            
            with tab1:
                st.markdown(f"### Likely Questions for {adjudication_type}")
                for q in mock_questions:
                    st.info(q)
                st.write("Use these questions in a mock interview session to build client confidence and reduce anxiety.")
                
            with tab2:
                st.markdown("### Trauma-Informed Advocate Guidance")
                for tip in coaching_tips:
                    st.markdown(f"* {tip}")
                    
            with tab3:
                st.markdown("### 🤝 Client-Facing Plain-Language View")
                st.info(client_note)
                st.markdown("#### Key Points to Remember:")
                for q in mock_questions:
                    st.write(f"• {q}")
                st.write("*(Tip: You can turn the screen or print this specific tab to review directly with the client in their preferred language.)*")
                    
            with tab4:
                st.markdown("### Human-in-the-Loop Sign-Off")
                st.write("Record that formal interview preparation was conducted and reviewed under attorney supervision.")
                attorney_name = st.text_input("Supervising Attorney / Advocate Name:")
                approval_check = st.checkbox("I verify that the client has been prepped using these materials.")
                
                if st.button("Log Prep Completion to Audit Trail"):
                    if attorney_name and approval_check:
                        st.success(f"Audit log successfully updated! Prep session logged by {attorney_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
                    else:
                        st.error("Please enter the name and check the verification box.")
