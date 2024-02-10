# Import necessary modules
from flask import Flask, request, jsonify
from functools import wraps
import json
import requests
import logging


# Initialize Flask app
app = Flask(__name__)

# log structure
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load users data from JSON file
USERS_DB_PATH = "users_db.json"
try:
    with open(USERS_DB_PATH, 'r') as file:
        users_data = json.load(file)
except FileNotFoundError:
    users_data = {}


# Load user access credentials from JSON file
USER_ACCESS_FILE = "users_access.json"
try:
    with open(USER_ACCESS_FILE, 'r') as file:
        user_access_data = json.load(file)
except FileNotFoundError:
    user_access_data = {}


# Basic authentication decorator
def basic_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            logger.warning("Authentication credentials missing or invalid")
            return jsonify({'message': 'Authentication required!'}), 401

        username, role = check_auth(auth.username, auth.password)
        if not username:
            logger.warning(f"Invalid credentials provided: {auth.username}")
            return jsonify({'message': 'Invalid credentials!'}), 401

        kwargs['username'] = username
        kwargs['role'] = role

        logger.info(f"User {username} authenticated with role {role}")
        return f(*args, **kwargs)
    return decorated_function


# Function to check if the provided credentials are valid
def check_auth(username, password):
    if username in user_access_data and user_access_data[username] == password:
        if "user" in username:
            return username, "user"
        elif username == "admin":
            return username, "admin"
    return None, None


# Function to check authorization using OPA
def check_authorization(method, path, role=None):
    OPA_URL = "http://localhost:8181/v1/data/opaweb/authz"
    input_data = {
        "method": method,
        "path": path,
        "authenticated": True if role else False,
        "role": role
    }
    try:
        response = requests.post(OPA_URL, json=input_data)
        if response.status_code == 200:
            result = response.json().get('result', False)
            return result
        else:
            return False  # If OPA service is unreachable or returns an error, deny the request
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to OPA service: {e}")
        return False  # If there's an exception while connecting to OPA, deny the request


# Endpoint to get users data (accessible only to authenticated users)
@app.route('/api/users', methods=['GET'])
@basic_auth_required
def get_users(username, role):
    if request.method != 'GET':
        logger.warning(f"Method not allowed for {request.method} request to /api/users")
        return jsonify({'message': 'Method not allowed!'}), 405

    logger.info(f"Accessing /api/users endpoint by {username} with role {role}")

    if check_authorization(request.method, request.path, role):
        return jsonify(users_data)
    else:
        logger.warning(f"Unauthorized access to /api/users by {username}")
        return jsonify({'message': 'Unauthorized access!'}), 403


# Endpoint to create user (accessible only to admin)
@app.route('/api/users', methods=['POST'])
@basic_auth_required
def create_user(username, role):
    if role != 'admin':
        return jsonify({'message': 'Only admin can create users!'}), 403

    if request.method != 'POST':
        logger.warning(f"Method not allowed for {request.method} request to /api/users")
        return jsonify({'message': 'Method not allowed!'}), 405

    logger.info(f"Creating user by admin: {username}")

    if check_authorization(request.method, request.path, role):
        data = request.get_json()
        if 'name' in data and 'email' in data:
            new_user = {
                'name': data['name'],
                'email': data['email']
            }
            users_data.append(new_user)  # Append the new user dictionary to the list
            with open(USERS_DB_PATH, 'w') as file:
                json.dump(users_data, file, indent=4)
            return jsonify({'message': 'User created successfully!'})
        else:
            return jsonify({'message': 'Name and email required!'}), 400
    else:
        logger.warning(f"Unauthorized access to /api/users by {username}")
        return jsonify({'message': 'Unauthorized access!'}), 403


# Function to run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
