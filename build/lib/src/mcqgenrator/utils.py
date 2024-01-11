import os
import json
import traceback
import PyPDF2

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        
        except Exception as e:
            raise Exception("Error: Kindly check pdf file again")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "Error: unspported file format only pdf and text file supported"
        )
        
def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict= json.loads(quiz_str)
        quiz_table_data = []
        
        # iterate over the quiz dictionary and extract the required information.
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option}->{option}" for option, option_value in value["options"].items()
                ]
            )
            
            correct = value["correct"]
            quiz_table_data.append({"MCQ":mcq,
                                    "Choices": options,
                                    "Correct": correct})
            
        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False