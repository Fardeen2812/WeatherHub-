from bcrypt import hashpw, gensalt, checkpw

# In-memory user storage
users = {}

def register_user(username, password):
    if username in users:
        return {'error': 'Username already exists'}, 400
    hashed_password = hashpw(password.encode(), gensalt())
    users[username] = {'username': username, 'password': hashed_password}
    return {'message': 'User registered successfully'}, 200

def authenticate_user(username, password):
    user = users.get(username)
    if user and checkpw(password.encode(), user['password']):
        return True
    return False