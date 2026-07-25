import streamlit as st
import openai
from datetime import datetime, date

st.set_page_config(page_title="1-Year Deadline Screener", page_icon="⏱️", layout="wide")

st.title("⏱️ 1-Year Statutory Filing Deadline Screener")
st.write("Calculate the one-year asylum filing deadline, check against current timeframes, and evaluate exception eligibility.")

# Initialize OpenAI client securely from Streamlit secrets
openai_api_key = st.secrets.get("OPENAI_API_KEY")

if not openai_api_key:
    st.warning("Please configure your OPENAI_API_KEY in your Streamlit app secrets.")
else:
    client = openai.OpenAI(api_key=openai_api_key)

    col1, col2 = st.columns(2)

    with col1:
        date_of_arrival = st.date_input("Date of Last Arrival in U.S.:", value=date(2025, 1, 15))

    with col2:
        # Calculate 1-year deadline (adding 365 days / 1 year approximately)
        try:
            deadline_date = date_of_arrival.replace(year=date_of_arrival.year + 1)
        except ValueError:
            # Handle leap year edge cases (e.g., Feb 29)
            deadline_date = date(date_of_arrival.year + 1, 3, 1)

        st.metric(label="Statutory 1-Year Filing Deadline", value=deadline_date.strftime("%B %d, %Y"))

    # Check status against current date
    today = date.today()
    days_remaining = (deadline_date - today).days

    if days_remaining < 0:
        st.error(f"⚠️ **DEADLINE PASSED:** The 1-year filing deadline was {abs(days_remaining)} days ago ({deadline_date.strftime('%B %d, %Y')}). A statutory exception must be established.")
    elif days_remaining <= 60:
        st.warning(f"⚠️ **URGENT:** Only {days_remaining} days remaining until the 1-year filing deadline!")
    else:
        st.success(f"✅ **Within Window:** {days_remaining} days remaining before the 1-year filing deadline.")

    st.divider()

    st.subheader("Evaluate Exceptions to the 1-Year Bar")
    st.write("If the 1-year deadline has passed, or is near, describe any potential changed or extraordinary circumstances.")

    exception_context = st.text_area(
        "Client Circumstances / Reason for Delay:",
        height=160,
        placeholder="E.g., Conditions in home country drastically worsened 6 months ago due to a coup, or client was incapacitated/minor during arrival..."
    )

    if st.button("Analyze Exception Viability"):
        if exception_context.strip():
            with st.spinner("Analyzing against statutory exceptions..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an expert immigration legal assistant. Analyze the provided narrative "
                                "against the two statutory exceptions to the 1-year asylum filing deadline: "
                                "1) Changed circumstances materially affecting eligibility, and "
                                "2) Extraordinary circumstances directly related to the failure to meet the 1-year deadline "
                                "(such as legal disability, ineffective assistance of counsel, or medical incapacity). "
                                "Provide a structured evaluation detailing potential strengths, evidentiary gaps, and the 'reasonable period' requirement."
                            )
                        },
                        {"role": "user", "content": exception_context}
                    ],
                    temperature=0.1
                )
                st.success("Exception analysis complete!")
                st.markdown("### Legal Exception Evaluation")
                st.markdown(response.choices[0].message.content)
        else:
            st.warning("Please enter details regarding the client's circumstances to run the analysis.")
