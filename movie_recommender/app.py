from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from models.user import User
from utils.db_config import Session
from models.tmdb_model import *
from utils.create_db import create_db


import hashlib
import os

app = Flask(__name__)

# Database session setup
create_db()
session = Session()

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
        session.add(new_user)
        session.commit()
    except IntegrityError:
        session.rollback()
        return jsonify({"error": "Username already exists."}), 409

    return jsonify({"message": "Account created successfully."}), 201

@app.route('/delete-user', methods=['DELETE'])
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

        print(username)

        if not username:
            return jsonify({'error': 'Invalid input, username is required'})

        # Call the User function to delete the user from the database
        User.delete_user(username)

        return jsonify({'status': 'user deleted', 'username': username})
    except Exception as e:
        return jsonify({'error': str(e)})


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
    user = session.query(User).filter(User.username == username).first()
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
    user = session.query(User).filter(User.username == username).first()
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
    session.commit()

    return jsonify({"message": "Password updated successfully."}), 200

@app.route('/get-recommendation-from-movies', methods=['POST'])
def get_recommendation_from_movies():
    """
    Get movie recommendations based on other movies.
    Expects JSON: {"title": "string"}
    """
    data = request.get_json()
    title = data.get('title')

    if not title:
        return jsonify({"error": "Title and region are required."}), 400

    # Get recommendations from TMDB
    recommendations = get_recommendations_from_movie(title)

    return jsonify({"recommendations": recommendations}), 200

@app.route('/get-recommendation-from-genre', methods=['POST'])
def get_recommendation_from_genre():
    """
    Get movie recommendations based on genre.
    Expects JSON: {"genre": "string"}
    """
    data = request.get_json()
    genre = data.get('genre')

    if not genre:
        return jsonify({"error": "Genre and region are required."}), 400

    # Get recommendations from TMDB
    recommendations = get_recommendations_for_genre(genre)

    return jsonify({"recommendations": recommendations}), 200

@app.route('/get-random-recommendation', methods=['POST'])
def get_random_recommendation_endpoint():
    """
    Get a random movie recommendation.
    Expects JSON: {"region": "string"}
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON input."}), 400

    region = data.get('region')
    if not region:
        return jsonify({"error": "Region is required."}), 400

    try:
        # Pass the region to the helper function
        recommendations = get_random_recommendation()

        # Respond appropriately if no recommendations are found
        if not recommendations:
            return jsonify({"message": "No recommendations found for the specified region."}), 200

        return jsonify({"recommendations": recommendations}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@app.route('/get-movie-summary', methods=['POST'])
def get_movie_summary_endpoint():
    """
    Get a summary of a movie.
    Expects JSON: {"title": "string"}
    """
    data = request.get_json()
    title = data.get('title')

    if not title:
        return jsonify({"error": "Title is required."}), 400

    # Get movie summary from TMDB
    summary = get_movie_summary(title)

    return jsonify({"summary": summary, "status": "ok"}), 200

@app.route('/get-trending-movies', methods=['POST'])
def get_trending_movies():
    """
    Get trending movies.
    Expects JSON: {"region": "string"}
    """
    data = request.get_json()
    region = data.get('region')

    if not region:
        return jsonify({"error": "Region is required."}), 400

    # Get trending movies from TMDB
    trending_movies = get_trending_movies_tmdb()

    return jsonify({"trending_movies": trending_movies, "status": "ok"}), 200

session.close()
if __name__ == '__main__':
    app.run(debug=True)
