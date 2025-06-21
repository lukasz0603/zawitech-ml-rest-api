from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Przykładowe współrzędne miast
CITY_COORDS = {
    "lublin": {"latitude": 51.25, "longitude": 22.57},
    "warszawa": {"latitude": 52.23, "longitude": 21.01},
    "krakow": {"latitude": 50.06, "longitude": 19.94},
    "wroclaw": {"latitude": 51.11, "longitude": 17.03}
}

@app.route("/predict", methods=["GET"])
def predict_weather():
    city = request.args.get("miasto", "").lower()

    if city not in CITY_COORDS:
        return jsonify({"error": "Nieobsługiwane miasto"}), 400

    coords = CITY_COORDS[city]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "forecast_days": 16,
        "timezone": "Europe/Warsaw"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        daily = data["daily"]
        result = []

        for i in range(len(daily["time"])):
            prob = daily["precipitation_probability_max"][i]
            risk = "WYSOKIE" if prob > 50 else "NISKIE"

            result.append({
                "data": daily["time"][i],
                "temp_max": daily["temperature_2m_max"][i],
                "temp_min": daily["temperature_2m_min"][i],
                "szansa_opadu": prob,
                "ryzyko": risk
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
