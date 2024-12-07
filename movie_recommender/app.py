from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from movie_recommender.utils.user import User
from models import SessionLocal
from utils import Session
from models import User

import hashlib
import os

app = Flask(__name__)

# Database session setup
db_session = SessionLocal()

@app.route('/health-check', methods=['GET'])
def health_check():
    """Verify the app is running."""
    return jsonify({"status": "ok"}), 200

@app.route('/create-account', methods=['POST'])
def create_account():
    """
    Create a new user account.
    Expects JSON: {"username": "string", "password": "string"}
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    # Generate salt and hashed password
    salt = os.urandom(16).hex()
    hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()

    # Create new user
    new_user = User(username=username, salt=salt, hashed_password=hashed_password)

    try:
        db_session.add(new_user)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "Username already exists."}), 409

    return jsonify({"message": "Account created successfully."}), 201

@app.route('/create-account', methods=['DELETE'])
def delete_user():
    """
        Delete an existing user account.
        Expects JSON: {"username": "string"}
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract and validate required fields
        username = data.get('username')

        if not username:
            return make_response(jsonify({'error': 'Invalid input, username is required'}), 400)

        # Call the User function to delete the user from the database
        app.logger.info('Deleting user: %s', username)
        Users.delete_user(username)

        app.logger.info("User deleted: %s", username)
        return make_response(jsonify({'status': 'user deleted', 'username': username}), 200)
    except Exception as e:
        app.logger.error("Failed to delete user: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/login', methods=['POST'])
def login():
    """
    Log in a user.
    Expects JSON: {"username": "string", "password": "string"}
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    # Retrieve user from the database
    user = db_session.query(User).filter(User.username == username).first()
    if not user:
        return jsonify({"error": "Invalid username or password."}), 401

    # Verify the password
    hashed_password = hashlib.sha256((user.salt + password).encode()).hexdigest()
    if hashed_password != user.hashed_password:
        return jsonify({"error": "Invalid username or password."}), 401

    return jsonify({"message": "Login successful."}), 200

@app.route('/update-password', methods=['POST'])
def update_password():
    """
    Update the user's password.
    Expects JSON: {"username": "string", "old_password": "string", "new_password": "string"}
    """
    data = request.get_json()
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not username or not old_password or not new_password:
        return jsonify({"error": "Username, old password, and new password are required."}), 400

    # Retrieve user from the database
    user = db_session.query(User).filter(User.username == username).first()
    if not user:
        return jsonify({"error": "Invalid username or password."}), 401

    # Verify the old password
    hashed_old_password = hashlib.sha256((user.salt + old_password).encode()).hexdigest()
    if hashed_old_password != user.hashed_password:
        return jsonify({"error": "Invalid old password."}), 401

    # Generate new salt and hashed password
    new_salt = os.urandom(16).hex()
    new_hashed_password = hashlib.sha256((new_salt + new_password).encode()).hexdigest()

    # Update the database
    user.salt = new_salt
    user.hashed_password = new_hashed_password
    db_session.commit()

    return jsonify({"message": "Password updated successfully."}), 200

def get_reccommendation_from_movies():
    pass;

def get_recommendation_from_genre():

if __name__ == '__main__':
    app.run(debug=True)
