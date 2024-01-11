import os
import json
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from src.mcqgenrator.utils import read_file, get_table_data
from src.mcqgenrator.logger import logging
from src.mcqgenrator.mcqgenrator import generate_evaluate_chain

# importing necessary pacakges from langchin
from langchain.callbacks import get_openai_callback

# loading json file
with open(r"F:\python\code\project\gan_project\mcq_gen\Response.json") as file:
    RESPONSE_JSON = json.load(file)
    
#Create a title for the app
st.title("MCQs Creator Applicatioon with LangChin....")

#Create a form using st.form
with st.form("user_inputs"):
    #File Upload
    upload_file = st.file_uploader("Upload a PDF or txt file")
    
    #Input Fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    
    #Subjects
    subject= st.text_input("Insert subject", max_chars=20)
    
    #Quiz Tone
    tone= st.text_input("Complexity Level of Questions", max_chars= 20, placeholder="simple")
    
    #Add Button
    button = st.form_submit_button("Create MCQs")
    
    #check if the button is clicked and all fields have inpit
    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading ..."):
            try:
                text = read_file(upload_file)
                
                #Count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(Response_JSON)
                        }
                    )
                #st.write(response)
            
            except Exception as e:
                traceback.print_exception(type(e), e, e.__teaceback__)
                st.error("Error")
                
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                    
                    #Extract the  quiz data from the response 
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            
                            #Display the review in atext box as well
                            st.text_area(label="review",
                                         value = response["review"])
                        else:
                            st.error("Error in the eable data")
                            
                else:
                    st.write(response)
                