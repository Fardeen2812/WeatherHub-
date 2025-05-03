from flask import Flask, render_template, request, jsonify
import requests
import os
import logging
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load BASE_URL and API keys from environment variables
BASE_URL = os.getenv('BASE_URL', 'http://localhost')
WEATHER_API_BASE_URL = os.getenv('WEATHER_API_BASE_URL', 'http://localhost')
RECOMMENDATION_ENGINE_BASE_URL = os.getenv('RECOMMENDATION_ENGINE_BASE_URL', 'http://localhost')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')  # Load OpenWeather API key

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = {}
    recommendation = {}
    message = "Enter a city name to get weather and recommendations."
    favicon = "sun.ico"  # Default favicon for sunny weather

    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if not city:
            return render_template('index.html', weather=weather, recommendation=recommendation, message="City name is required", favicon=favicon)

        try:
            weather = requests.get(f"{WEATHER_API_BASE_URL}:5001/weather?city={city}").json()
            logging.info(f"Weather data fetched for city: {city}")
            if 'weather' in weather and len(weather['weather']) > 0:
                condition = weather['weather'][0]['main'].lower()
                # Map weather conditions to favicon files
                if 'clear' in condition:
                    favicon = "sun.ico"
                elif 'cloud' in condition:
                    favicon = "cloudy.ico"
                elif 'rain' in condition:
                    favicon = "rain.ico"
                elif 'snow' in condition:
                    favicon = "snowflake.ico"
                else:
                    favicon = "cloud.ico"  # Default for unknown cloudy weather
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching weather data: {e}")
            weather = {"error": "Weather service is unavailable"}

        try:
            recommendation = requests.get(f"{RECOMMENDATION_ENGINE_BASE_URL}:5003/recommendation?city={city}").json()
            logging.info(f"Recommendation data fetched for city: {city}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching recommendation data: {e}")
            recommendation = {"error": "Recommendation service is unavailable"}

    return render_template('index.html', weather=weather, recommendation=recommendation, message=message, favicon=favicon)

@app.route('/city-suggestions', methods=['GET'])
def city_suggestions():
    query = request.args.get('q', '')
    if len(query) < 3:
        return jsonify([])

    url = f"https://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={OPENWEATHER_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching city suggestions: {e}")
        return jsonify([]), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)
