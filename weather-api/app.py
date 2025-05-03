from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City is required'}), 400
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    logging.info(f"OpenWeather API response: {response.json()}")
    return jsonify(response.json())

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Weather API!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
