import json
import requests
import pprint
from getComponents import getComponent
import sys
sys.path.append('../mail_tokenizer')
import clasification
import spacy
import joblib
import streamlit as st

nlp = spacy.load('en_core_web_sm')

st.set_page_config(layout="wide")

def spacy_tokenizer(text):
    tokens = nlp(text)
    return [token.lemma_.lower() for token in tokens if not token.is_punct and not token.is_stop]



components = getComponent()

loaded_pipeline = joblib.load("/Users/aleksandar.bajceta/src/mail-classifier/classification_model.joblib")


def create_status_page(text):
    result = clasification.predict(loaded_pipeline, text)

    if result == 0:
        print('not creating')
        return False
    
    return clasification.get_data(text[0])


def send_status(data):
    if data == False:
        return
    name = data.get_bank_name()
    body = data.get_product()
    componentId = components[name]


    postIncidentURL = "https://api.statuspage.io/v1/pages/DUMMYPAGE/incidents"
    headers = {"Authorization": "OAuth dummyOne"}
    data = {
    "incident": {
        "name": name+" -  Major Outage affecting "+body,
        "status": "investigating",
        "body": body,
        "component_ids": [componentId],
        }
    }
    r = requests.post(url=postIncidentURL, json=data, headers=headers)


st.write(""" # SNSSSPUA \n Simple not so smart status page update app """)


txt = st.text_area('Text to analyze', height=500)

if st.button("Run analysis"):
    print(txt)
    send_status(create_status_page([txt]))

