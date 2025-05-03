from flask import Flask, request, jsonify
import jwt
import datetime
import os
from bcrypt import hashpw, gensalt, checkpw
import psycopg2

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret')

users = {}

conn = psycopg2.connect(
    dbname="user_preferences",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT, preferences JSONB)")
conn.commit()

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the User Preference API!",
        "usage": {
            "register": "POST /register with JSON payload {'username': <username>, 'password': <password>}",
            "login": "POST /login with JSON payload {'username': <username>, 'password': <password>}"
        }
    })

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return an empty response with a 204 No Content status

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if data['username'] in users:
        return jsonify({'error': 'Username already exists'}), 400
    hashed_password = hashpw(data['password'].encode(), gensalt())
    users[data['username']] = {'username': data['username'], 'password': hashed_password}
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users.get(data['username'])
    if user and checkpw(data['password'].encode(), user['password']):
        token = jwt.encode({'username': data['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
