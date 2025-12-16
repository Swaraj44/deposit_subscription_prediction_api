from model_class import AdvancedBankMarketingPredictor
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import joblib
from contextlib import asynccontextmanager
from config.data_processing import data_process_for_pred
from schema.user_input import UserInput


app = FastAPI(
    title="Smart Banking Term-Deposit Response Prediction API",
    version="1.0",
    description="Predict term deposit subscription"
)


MODEL_PATH = "model/bank_model.pkl"
model = joblib.load(MODEL_PATH)

@app.post('/predict')
def predict_premium(data: UserInput):

    input_df = pd.DataFrame([{
        "age": data.age,
        "job": data.job,
        "marital": data.marital,
        "education": data.education,
        "default": data.default,
        "balance": data.balance,
        "housing": data.housing,
        "loan": data.loan,
        "contact": data.contact,
        "day_of_week": data.day_of_week,
        "month": data.month,
        "duration": data.duration,
        "campaign": data.campaign,
        "pdays": data.pdays,
        "previous": data.previous,
        "poutcome": data.poutcome
    }])

    input_data_fe, input_data_en = data_process_for_pred(input_df)
    
    input_data_proba = model.predict_proba(input_data_fe, input_data_en)[0]
    input_data_pred = int(input_data_proba >= model.best_threshold)
 

    return JSONResponse(
        status_code=200,
        content={
            'predicted_category': input_data_pred,
            'predicted_probability': input_data_proba
        }
    )


@app.get('/')
def home():  
    return {
        'message': 'Welcome to Smart Banking Term-Deposit Response Prediction Engine'
    }



@app.get("/health")
def health_check():
    return {
        'status': 'ok',
        'model_version': '1.0'
    }
