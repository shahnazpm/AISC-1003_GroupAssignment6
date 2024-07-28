import json
import requests
import streamlit as st
import pandas as pd
from PIL import Image
import pickle
from flask import Flask

# app = Flask(__name__)

# Load pre-trained model
model_file = 'svm.pkl'
with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)
 
input_dict = {}

# Define feature names
feature_names = ['AMOUNT_RUB_SUP_PRC', 'REST_AVG_CUR', 'TRANS_COUNT_ATM_PRC', 'AMOUNT_RUB_ATM_PRC',
                 'CNT_TRAN_CLO_TENDENCY3M', 'REST_DYNAMIC_CUR_1M', 'SUM_TRAN_SUP_TENDENCY1M', 'CNT_TRAN_SUP_TENDENCY1M',
                 'CLNT_SETUP_TENOR', 'TRANS_AMOUNT_TENDENCY3M']
 
# Create Streamlit app
st.title("Predicting Customer Churn")
 
# Create input form
with st.form('input_form'):
    AMOUNT_RUB_SUP_PRC = st.number_input('AMOUNT_RUB_SUP_PRC:', min_value=-6.0, max_value=1.0, value=0.0)
    REST_AVG_CUR = st.number_input('REST_AVG_CUR:', min_value=-6.0, max_value=1.0, value=0.0)
    TRANS_COUNT_ATM_PRC = st.number_input('TRANS_COUNT_ATM_PRC:', min_value=0, max_value=1, value=0)
    AMOUNT_RUB_ATM_PRC = st.number_input('AMOUNT_RUB_ATM_PRC:', min_value=-6.0, max_value=1.0, value=0.0)
    CNT_TRAN_CLO_TENDENCY3M = st.number_input('CNT_TRAN_CLO_TENDENCY3M:', min_value=0, max_value=1, value=0)
    REST_DYNAMIC_CUR_1M = st.number_input('REST_DYNAMIC_CUR_1M:', min_value=-6.0, max_value=1.0, value=0.0)
    SUM_TRAN_SUP_TENDENCY1M = st.number_input('SUM_TRAN_SUP_TENDENCY1M:', min_value=-6.0, max_value=1.0, value=0.0)
    CNT_TRAN_SUP_TENDENCY1M = st.number_input('CNT_TRAN_SUP_TENDENCY1M:', min_value=0, max_value=1, value=0)
    CLNT_SETUP_TENOR = st.number_input('CLNT_SETUP_TENOR:', min_value=0, max_value=1, value=0)
    TRANS_AMOUNT_TENDENCY3M = st.number_input('TRANS_AMOUNT_TENDENCY3M:', min_value=-6.0, max_value=1.0, value=0.0)
 
    # Create submit button
    submit_button = st.form_submit_button('Predict Churn')
 
# Make prediction on submit
if submit_button:
    input_dict = {
        "AMOUNT_RUB_SUP_PRC": AMOUNT_RUB_SUP_PRC,
        "REST_AVG_CUR": REST_AVG_CUR,
        "TRANS_COUNT_ATM_PRC": TRANS_COUNT_ATM_PRC,
        "AMOUNT_RUB_ATM_PRC": AMOUNT_RUB_ATM_PRC,
        "CNT_TRAN_CLO_TENDENCY3M": CNT_TRAN_CLO_TENDENCY3M,
        "REST_DYNAMIC_CUR_1M": REST_DYNAMIC_CUR_1M,
        "SUM_TRAN_SUP_TENDENCY1M": SUM_TRAN_SUP_TENDENCY1M,
        "CNT_TRAN_SUP_TENDENCY1M": CNT_TRAN_SUP_TENDENCY1M,
        "CLNT_SETUP_TENOR": CLNT_SETUP_TENOR,
        "TRANS_AMOUNT_TENDENCY3M": TRANS_AMOUNT_TENDENCY3M,
    }
 
# Convert input dictionary to JSON
input_json = json.dumps(input_dict)
 
# Make POST request to Flask API
response = requests.post('http://127.0.0.1:5000/prediction', json=input_json)
 
# Get prediction from response
prediction = response.json()['result']
# churn_probability = response.json()['churn_probability']

# Display prediction
st.write('prediction:', prediction)
# st.write('Churn Probability:', churn_probability)
 
# Display image based on prediction
if prediction == 'Prediction: 1':
  st.write('Customer is likely to churn')
else:
  st.write('Customer is unlikely to churn')
