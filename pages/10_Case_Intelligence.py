"🧠 Case Intelligence & Adversarial Review",
elif workflow_tab == "🧠 Case Intelligence & Adversarial Review":

    st.subheader("🧠 Immigration Case Intelligence")

    st.caption(
        "Builds a structured case record from source material, "
        "then stress-tests the case for factual and evidentiary vulnerabilities."
    )

    case = st.session_state.case

    st.write(f"**Case ID:** `{case.case_id}`")

    source_type = st.selectbox(
        "Source type",
        [
            "client_statement",
            "voice_note",
            "whatsapp",
            "document",
            "email",
        ],
    )

    source_name = st.text_input(
        "Source name",
        placeholder="WhatsApp Voice Note 03"
    )

    source_text = st.text_area(
        "Paste transcript / extracted text",
        height=250,
    )

    if st.button(
        "Extract Facts Into Case Memory",
        type="primary",
    ):

        if not source_text.strip():
            st.warning("Provide source text first.")

        else:

            source = Source(
                source_id=str(uuid.uuid4()),
                source_type=source_type,
                name=source_name or "Unnamed Source",
                excerpt=source_text[:500],
            )

            with st.spinner(
                "Extracting source-grounded facts..."
            ):

                case = agents.extract_facts(
                    case,
                    source_text,
                    source,
                )

                case = agents.build_timeline(case)

                st.session_state.case = case

            st.success(
                f"Added {len(case.facts)} facts to case memory."
            )

    st.divider()

    st.markdown("### 📋 Case Facts")

    for fact in case.facts:

        status = (
            "✅ Attorney verified"
            if fact.attorney_verified
            else "⚠️ Unverified"
        )

        st.markdown(
            f"""
**{fact.statement}**

- Fact ID: `{fact.fact_id}`
- Date: `{fact.date or "Not established"}`
- Confidence: `{fact.confidence}`
- Source(s): `{", ".join(fact.sources)}`
- Status: {status}
"""
        )

    st.divider()

    if st.button(
        "🔴 Attack This Case",
        type="secondary",
    ):

        with st.spinner(
            "Running adversarial consistency review..."
        ):

            vulnerabilities = find_potential_contradictions(
                client,
                case,
            )

            case.vulnerabilities.extend(
                vulnerabilities
            )

            st.session_state.case = case

    if case.vulnerabilities:

        st.markdown("### 🚨 Potential Case Vulnerabilities")

        for issue in case.vulnerabilities:

            if issue.severity in ["critical", "high"]:
                st.error(
                    f"**{issue.severity.upper()} — {issue.issue}**\n\n"
                    f"{issue.explanation}\n\n"
                    f"**Recommended action:** "
                    f"{issue.recommended_action or 'Attorney review required.'}"
                )

            else:
                st.warning(
                    f"**{issue.severity.upper()} — {issue.issue}**\n\n"
                    f"{issue.explanation}"
                )

    st.divider()

    st.markdown("### 🕒 Case Timeline")

    for event in case.timeline:

        st.markdown(
            f"""
**{event.date or "Date unknown"}**

{event.description}

Source(s): `{", ".join(event.sources)}`
"""
        )
