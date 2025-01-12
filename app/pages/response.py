import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

st.title("📧 Mail Response Generator")
mail_input = st.text_input("Enter the mail content:", value=" ")
res_input = st.text_input("Enter the response:", value=" ")
submit_button = st.button("Submit")
response_placeholder = st.empty()
copy_placeholder = st.empty()
if submit_button:
        try:
            llm = ChatGroq(temperature=0, groq_api_key=os.getenv("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"), model_name="llama-3.1-70b-versatile")
            prompt_extract = PromptTemplate.from_template(
            """
            ### EMAIL RECEIVED:
            {mail_input}
            
            ### REQUIRED RESPONSE CONTENT:
            {res_input}
            
            ### INSTRUCTION:
            Draft a professional email response to the above email. The response should:
            1. Address the sender politely and professionally based on the context of the received email.
            2. Include the "REQUIRED RESPONSE CONTENT" ({res_input}) as part of the body of the email in a natural and coherent way.
            3. Maintain a professional and formal tone throughout the email.
            4. Ensure clarity, grammatical accuracy, and proper formatting.

            Structure the email as follows:
            - **Subject**: A concise and relevant subject line for the response.
            - **Greeting**: Start with a professional salutation (e.g., "Dear [Name],").
            - **Body**: Incorporate the details from "REQUIRED RESPONSE CONTENT" while addressing the key points from the received email.
            - **Closing**: End with a polite closing statement and a professional sign-off.

            Generate only the final email text without any explanations or preambles.
            """
            )
            chain_extract = prompt_extract | llm
            res = chain_extract.invoke(input={"mail_input": mail_input,"res_input": res_input})
            generated_response = res.content

            # Display the response in a text area
            response_placeholder.text_area("Generated Response:", value=generated_response, height=300, disabled=True)

            # Add a copy button
            if copy_placeholder.button("Copy Email"):
                st.session_state.clipboard = generated_response  # Save in session state
                st.success("Email copied to clipboard!")
                #st.markdown(f"### Generated Response:\n\n{res.content}")
        except Exception as e:
            st.error(f"An Error Occurred: {e}")