# app.py
from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route("/predict", methods=["GET"])
def predict_rain():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.23,  # Warszawa
        "longitude": 21.01,
        "hourly": "precipitation_probability",
        "forecast_days": 1
    }

    response = requests.get(url, params=params)
    data = response.json()
    hourly = data['hourly']

    prediction = []
    for time, prob in zip(hourly["time"], hourly["precipitation_probability"]):
        risk = "WYSOKIE" if prob > 50 else "NISKIE"
        prediction.append({
            "czas": time,
            "szansa_opadu": prob,
            "ryzyko": risk
        })

    return jsonify(prediction)
