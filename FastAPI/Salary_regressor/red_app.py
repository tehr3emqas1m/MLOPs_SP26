# app.py
import joblib
import pandas as pd
from fastapi import FastAPI

model = joblib.load("model.pkl")
app = FastAPI(title="Salary Predictor API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: dict):
    experience = float(payload["experience"])
    X = pd.DataFrame({"experience": [experience]})
    prediction = float(model.predict(X)[0])
    return {"experience": experience, "prediction": prediction}