from flask import Flask, request, jsonify
import redis
import json
import os
import re
import logging
from redis.exceptions import RedisError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

redis_host = os.getenv("REDIS_HOST")
redis_password = os.getenv("REDIS_PASSWORD")

redis_client = redis.StrictRedis(host=redis_host, port=6379, password=redis_password, decode_responses=True)

# Initialize Flask app
app = Flask(__name__)

# Initialize Redis cache
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379)

# Initialize rate limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per minute"])

# Configure logging
logging.basicConfig(level=logging.INFO)

# Predefined recommendations for the top 50 popular cities
TOP_50_CITIES = {
    "london": "Carry an umbrella",
    "new york": "Visit Central Park",
    "paris": "Enjoy the Eiffel Tower",
    "tokyo": "Explore Shibuya Crossing",
    "dubai": "Visit the Burj Khalifa",
    "singapore": "Take a walk at Marina Bay Sands",
    "sydney": "Enjoy the Sydney Opera House",
    "los angeles": "Walk along Hollywood Boulevard",
    "rome": "Explore the Colosseum",
    "barcelona": "Visit the Sagrada Familia",
    "moscow": "Take a tour of the Kremlin",
    "beijing": "Walk along the Great Wall of China",
    "mumbai": "Enjoy the Gateway of India",
    "rio de janeiro": "Relax at Copacabana Beach",
    "cape town": "Hike up Table Mountain",
    "istanbul": "Visit the Hagia Sophia",
    "shanghai": "Explore the Bund",
    "berlin": "Visit the Berlin Wall",
    "amsterdam": "Take a canal cruise",
    "toronto": "Enjoy the CN Tower",
    "san francisco": "Walk across the Golden Gate Bridge",
    "chicago": "Visit Millennium Park",
    "hong kong": "Take the Star Ferry",
    "bangkok": "Explore the Grand Palace",
    "seoul": "Visit Gyeongbokgung Palace",
    "mexico city": "Explore the Zócalo",
    "delhi": "Visit the Red Fort",
    "jakarta": "Enjoy the National Monument",
    "kuala lumpur": "Visit the Petronas Towers",
    "cairo": "Explore the Pyramids of Giza",
    "madrid": "Visit the Royal Palace",
    "lisbon": "Take a tram ride through the city",
    "vienna": "Enjoy Schönbrunn Palace",
    "prague": "Walk across Charles Bridge",
    "athens": "Explore the Acropolis",
    "buenos aires": "Visit the Casa Rosada",
    "são paulo": "Enjoy Ibirapuera Park",
    "zurich": "Relax by Lake Zurich",
    "stockholm": "Visit the Vasa Museum",
    "oslo": "Explore the Viking Ship Museum",
    "helsinki": "Visit Suomenlinna Fortress",
    "copenhagen": "Enjoy Tivoli Gardens",
    "budapest": "Relax at the thermal baths",
    "warsaw": "Explore the Old Town",
    "dublin": "Visit the Guinness Storehouse",
    "edinburgh": "Walk along the Royal Mile",
    "venice": "Take a gondola ride",
    "florence": "Admire Michelangelo's David",
    "munich": "Enjoy a beer at Oktoberfest",
    "seattle": "Visit the Space Needle"
}

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Recommendation Engine API!",
        "usage": "Use the /recommendation endpoint with a 'city' query parameter to get recommendations.",
        "example": "/recommendation?city=London"
    })

@app.route('/recommendation')
@limiter.limit("10 per minute")  # Limit to 10 requests per minute per client
def recommend():
    city = request.args.get('city')
    if not city:
        logging.warning("City parameter is missing")
        return jsonify({'error': 'City parameter is required'}), 400

    # Validate city input
    if not re.match("^[a-zA-Z ]+$", city):
        logging.warning(f"Invalid city name: {city}")
        return jsonify({'error': 'Invalid city name'}), 400

    city_lower = city.lower()

    try:
        # Check if the recommendation is cached
        cached = cache.get(city_lower)
        if cached:
            logging.info(f"Cache hit for city: {city_lower}")
            return jsonify(json.loads(cached))
    except RedisError as e:
        logging.error(f"Redis error: {str(e)}")
        return jsonify({'error': 'Cache service is unavailable'}), 503

    # Check if the city is in the top 50 popular cities
    if city_lower in TOP_50_CITIES:
        recommendations = {"message": TOP_50_CITIES[city_lower]}
    else:
        # Default recommendation logic for other cities
        recommendations = {"message": "Enjoy your day!"}

    try:
        # Cache the recommendation
        cache.set(city_lower, json.dumps(recommendations), ex=3600)  # Cache for 1 hour
        logging.info(f"Cache set for city: {city_lower}")
    except RedisError as e:
        logging.error(f"Failed to cache recommendation for city: {city_lower} - {str(e)}")

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
