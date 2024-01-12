import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
# from mcqgenrator.utils import read_file, get_table_data
# from mcqgenrator.logger import logging

# importing necessary pacakges from langchin
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain


# load enviroment variables from .env file
load_dotenv()

# Access the enviroment variables just like you would with os.envirom
Key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key= Key,
                 model_name="gpt-3.5-turbo",
                 temperature= 0.5)

# prompt is two kinds of 
# 1) zero short prompt- dirctly asking question from llm model
# few Prompt- in this some short of direction which using for creat response according ginven direction.  
TEMPLATE_1 = """ 
Text:{text}
You are an expert MCQ maker. Give  the above text, it is your job to \
    creat a quiz of {number}multiple choice questions for {subject} students in {tone} tone.
    Make sure the question are not repeated and check all the question to be conforming the text as well.
    Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
    Ensure to make {number} MCQs
    ### RESPONSE_JSON
    {response_json}"""
    
quiz_gen_prompts = PromptTemplate(
    input_variables = ["text", "number", "subject", "tone", "response_json"],
    template = TEMPLATE_1
)

quize_chain = LLMChain(llm = llm,
                       prompt = quiz_gen_prompts,
                       output_key="quiz",
                       verbose=True
                       )

# Quize evaluations
TEMPLATE_2 = """ 
You are an export english grammarian and writer. Give a Multiple ahoice Quize for {subject} students.\
    You need to evaluate the complexity of the question and give a complete analysis of the quize. Only use at max 50 words for complexity.\
    if the quize is not at per with the cognitive and analytical avilities of the students,\
    update the quize question which needs to be changed and change the tone such that it perfectly fit the student abilities
    Quiz_MCQ:
    {quiz}
       
    check from an expert English writer of the above quiz:
    """
       
quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template = TEMPLATE_2
    )

review_chain = LLMChain(llm = llm, 
                        prompt= quiz_evaluation_prompt,
                        output_key = "review",
                        verbose = True
                        )

generate_evaluate_chain = SequentialChain(chains=[quize_chain, review_chain], 
                                         input_variables = ["text", "number", "subject", "tone", "response_json"],
                                         output_variables = ["quiz","review"],
                                         verbose = True
                                         )

