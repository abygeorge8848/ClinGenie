from flask import request
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from openai import ChatCompletion
import openai
import os
from dotenv import load_dotenv
load_dotenv()


def gpt(app):

    @app.route('/gpt/test')
    def gpt_test():
        return 'Test GPT Working!'

    @app.route('/gpt/completions', methods=['POST'])
    def gpt_completions():
        index = int(request.get_json()['databaseValue'])

        data_dictionary = ["""
            # dsp_data(disease, symptom_1, symptom_2, symptom_3,symptom_4, symptom_5)
            # dsp_symp_description(disease, description)
            # dsp_symp_precaution(disease, precaution_1, precaution_2, precaution_3, precaution_4)
            # dsp_symp_severity(symptom, weight)
        """, """
            # CVD_data ( General_Health TEXT, Checkup TEXT, Exercise TEXT, Heart_Disease TEXT, Skin_Cancer TEXT, Other_Cancer TEXT, Depression TEXT, Diabetes TEXT, Arthritis TEXT, Sex TEXT, Age_Category TEXT, Height_(cm) REAL, Weight_(kg) REAL, BMI REAL, Smoking_History TEXT, Alcohol_Consumption REAL, Fruit_Consumption REAL, Green_Vegetables_Consumption REAL, FriedPotato_Consumption REAL )
        """, """
            # Sleep_health_data('Person ID', 'Gender', 'Age', 'Occupation', 'Sleep Duration', 'Quality of Sleep', 'Physical Activity Level', 'Stress Level', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps', 'Sleep Disorder')
        """]


        selected_dataset = data_dictionary[index]

        prompt = """
            You are a SQL expert, and your role is to generate an SQLite3 statement to answer users questions,
            based on the dataset below: 

            DATASET

            Follow the following rules while generating the SQL statement:
            1. Make all where clauses case-insensitive. 
            2. Handle common mis-spellings. 
            3. Handle common synonyms.
            4. Round all aggregate functions like average, sum, etc to 2 decimal places. For example, ROUND(AVG(ColumnName), 2).
            5. Return only the SQL statement. Even if the user asks for a plot, chart or graph, you should return a SQL statement only.

        """.replace('DATASET', selected_dataset)
    
        query = request.get_json()['query']

        return gpt_call(prompt, query)



def get_text(cols_and_data):
    prompt = """
            You are an English expert. 
            Given a users question, and data in the form of columns and data, 
            you need to write a sentence that answers the question.
        """
    return gpt_call(prompt, cols_and_data)



def set_token_from_azure_cred():
    ad_programmatic_scope = os.getenv('AD_PROGRAMMATIC_SCOPE')
    deployment_id = os.getenv('DEPLOYMENT_ID')
    openai.api_type = os.getenv('OPENAI_API_TYPE')
    openai.api_base = os.getenv('OPENAI_API_BASE')
    openai.api_version = os.getenv('OPENAI_API_VERSION')

    credentials = DefaultAzureCredential()
    token = credentials.get_token(ad_programmatic_scope)
    # print(f'Token: {token}')
    openai.api_key = token.token
    return deployment_id



def gpt_call(prompt, query):
    deployment_id = set_token_from_azure_cred()

    response = ChatCompletion.create(
        deployment_id=deployment_id,
        model='gpt-4',
        temperature=0,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ],
    )

    return response