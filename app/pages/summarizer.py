import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from pymongo import MongoClient

mongo_uri= "mongodb+srv://chanaveer7:123@cluster0.6iy7n.mongodb.net/"
client = MongoClient(mongo_uri)

db= client['email']
collection = db['jobs']

st.title("📧 Mail Response Generator")
mail_input = st.text_input("Enter the mail content:", value=" ")
submit_button = st.button("Submit")

if submit_button:
        try:
            llm = ChatGroq(temperature=0, groq_api_key=os.getenv("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"), model_name="llama-3.1-70b-versatile")
            prompt_extract = PromptTemplate.from_template(
            """
            ### EMAIL CONTENT:
            {mail_input}
            
            ### INSTRUCTION:
            Analyze the email and summarize it effectively. Use JSON format internally to organize the following:
            - The purpose of the email.
            - Key details or important points mentioned.
            - Any action items, requests, or follow-ups required (if any).
            the above three points should be hilighted in output
            Based on this internal JSON structure, generate a well-organized textual summary that can be directly displayed. Ensure the summary is:
            - Concise and to the point.
            - Clearly structured for easy understanding.
            - Suitable for direct presentation to a user.
            
            in the output don't ever mention json 
            write the summary is less than 200 words
            """
            )
            chain_extract = prompt_extract | llm
            res = chain_extract.invoke(input={"mail_input": mail_input})
            summary = {
                 'email': mail_input,
                 'response': res.content,
            }
            collection.insert_one(summary)
            st.markdown(f"### Generated Response:\n\n{res.content}")
            # st.code(res.content, language='markdown')
            #st.text_area("Generated Response:", value=res.content, height=300,disabled=True)
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


st.title('history')
summary= collection.find()
for sum in summary:
     st.write(sum)