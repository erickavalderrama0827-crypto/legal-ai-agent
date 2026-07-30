elif workflow_tab == "✉️ Automated Intake Email Generator":
            st.subheader("✉️ Automated Intake Email & Follow-Up Generator")
            st.write("Generate professional, multi-lingual follow-up emails and information requests for clients.")

            client_name = st.text_input("Client Name:", placeholder="e.g., Elena Morales")
            preferred_language = st.selectbox("Preferred Language:", ["English", "Spanish", "French", "Haitian Creole"])
            email_purpose = st.text_input("Email Purpose:", placeholder="e.g., Document Request & Follow-up")
            specific_details = st.text_area("Specific Details to Include:", height=130, placeholder="e.g., Need certified copies of police reports from Tegucigalpa and remind her of our upcoming meeting next Tuesday...")

            if st.button("Generate Professional Intake Email 🚀", type="primary"):
                if client_name.strip() and email_purpose.strip() and specific_details.strip():
                    with st.spinner("Drafting professional, trauma-informed multi-lingual client correspondence..."):
                        try:
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": (
                                            "You are an expert immigration legal assistant and communications specialist. "
                                            "Draft a professional, empathetic, and clear client follow-up email based on the inputs. "
                                            "The email must be written entirely in the client's preferred language. "
                                            "Include appropriate subject lines, respectful greetings, clear action items, and office contact sign-offs."
                                        )
                                    },
                                    {
                                        "role": "user",
                                        "content": f"Client Name: {client_name}\nPreferred Language: {preferred_language}\nEmail Purpose: {email_purpose}\nSpecific Details: {specific_details}"
                                    }
                                ],
                                temperature=0.0
                            )
                            # Capture the actual generated text string from the OpenAI response object
                            email_output = response.choices[0].message.content
                            
                            st.success("Client Email Generated Successfully!")
                            st.markdown("---")
                            st.markdown("### 📨 Drafted Correspondence")
                            
                            # Render the actual output text on the page so it shows up
                            st.markdown(email_output)
                            
                            st.download_button(
                                label="📥 Download Intake Email (.txt)",
                                data=email_output,
                                file_name=f"Intake_Email_{client_name.replace(' ', '_')}.txt",
                                mime="text/plain"
                            )
                            
                            st.markdown("---")
                            st.markdown("### 🔒 Human-in-the-Loop (HITL) Sign-Off")
                            st.checkbox("Attorney/Staff Verification: Review and approve email draft before sending to client.")
                            
                        except Exception as e:
                            st.error(f"OpenAI API Error: {e}. Please check your API key secrets in Streamlit.")
                else:
                    st.warning("⚠️ Please fill out all required fields to generate the email.")
