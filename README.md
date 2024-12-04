# Movie Recommendation System

## Overview
The Movie Recommendation System is a web application designed to provide personalized movie recommendations, allow users to search for movies, and maintain a personal watchlist. This project utilizes Flask for the backend, SQLite for data storage, and the TMDB (The Movie Database) API for movie data.

## Features
- **Account Management**:
  - Create a new account, log in, and update passwords securely.
- **Movie Recommendations**:
  - Get movie recommendations based on genres or user preferences.
- **Watchlist Management**:
  - Add movies to a personal watchlist and retrieve it anytime.
- **Movie Search**:
  - Search for movies by title or keywords.
- **Trending Movies**:
  - Discover movies trending in the user's region.

## Routes

### 1. `/create-account`
- **Request Type**: `POST`
- **Purpose**: Create a new user account.
- **Request Format**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response Format**:
  ```json
  {
    "message": "Login successful."
  }
  ```

### 2. `/login`
- **Request Type**: `POST`
- **Purpose**: Log in to an existing user account.
- **Request Format**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response Format**:
  ```json
  {
    "message": "Login successful."
  }
  ```

### 3. `/update-password`
- **Request Type**: `POST`
- **Purpose**: Update the user's password.
- **Request Format**:
  ```json
  {
    "username": "string",
    "old_password": "string",
    "new_password": "string"
  }
  ```
- **Response Format**:
  ```json
  {
    "message": "Password updated successfully."
  }
  ```

### 4. `/get-recommendations`
- **Request Type**: `POST`
- **Purpose**: Get movie recommendations based on genre and region.
- **Request Format**:
  ```json
  {
    "genre": "string",
    "region": "string"
  }
  ```
- **Response Format**:
  ```json
  {
    "recommendations": [
      {
        "title": "string",
        "overview": "string",
        "release_date": "string"
      }
    ]
  }
  ```

### 5. `/add-to-watchlist`
- **Request Type**: `POST`
- **Purpose**: Add a movie to the user's watchlist.
- **Request Format**:
  ```json
  {
    "username": "string",
    "movie_id": "int"
  }
  ```
- **Response Format**:
  ```json
  {
    "message": "Movie added to watchlist."
  }
  ```

### 6. `/get-watchlist`
- **Request Type**: `POST`
- **Purpose**: Retrieve the user's watchlist.
- **Request Format**:
  ```json
  {
    "username": "string"
  }
  ```
- **Response Format**:
  ```json
  {
    "watchlist": [
      {
        "title": "string",
        "overview": "string",
        "release_date": "string",
        "rating": "float"
      }
    ]
  }
  ```