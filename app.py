import streamlit as st

# 1. Sidebar Navigation Toggle for the Meeting
st.sidebar.title("Primer Paso AI")
page = st.sidebar.radio("Navigation", ["🏠 Home / Overview", "⚡ Live Workflow Tool"])

if page == "🏠 Home / Overview":
    # --- LANDING PAGE VIEW ---
    st.title("Primer Paso AI")
    st.subheader("Streamlining Legal Intake & Timeline Verification")

    st.write(
        "Welcome to the platform overview. Primer Paso AI automates "
        "multi-lingual legal intake and timeline cross-checking to accelerate "
        "case preparation."
    )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🌐 Multi-Lingual Intake")
        st.write("Seamless translation and structured extraction for diverse clients.")
    with col2:
        st.markdown("### ⏱️ Timeline Verification")
        st.write("Automated date cross-checking to spot discrepancies instantly.")

    st.markdown("---")
    if st.button("Launch Application Workspace 🚀", type="primary"):
        # This trick switches the radio state programmatically if desired, 
        # or you can just tell them to click the sidebar.
        st.info("Select '⚡ Live Workflow Tool' from the sidebar to jump in!")

elif page == "⚡ Live Workflow Tool":
    # --- YOUR EXISTING APP CODE GOES RIGHT HERE ---
    st.title("Workflow Workspace")
    
    # Paste the rest of your current multi-agent/intake code below:
    st.write("*(Your existing tool functionality lives here...)*")
