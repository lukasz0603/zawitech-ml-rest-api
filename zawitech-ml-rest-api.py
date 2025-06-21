from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["GET"])
def predict_rain():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 51.25,  # Lublin
        "longitude": 22.57,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "forecast_days": 30,
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()
    daily = data['daily']

    prediction = []
    for i in range(len(daily["time"])):
        prob = daily["precipitation_probability_max"][i]
        risk = "WYSOKIE" if prob > 50 else "NISKIE"
        prediction.append({
            "data": daily["time"][i],
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "szansa_opadu": prob,
            "ryzyko": risk
        })

    return jsonify(prediction)
