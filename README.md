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

### 4. `/get-recommendation-from-movies`
- **Request Type**: `POST`
- **Purpose**: Get movie recommendations based other movies.
- **Request Format**:
  ```json
  {
    "title": "string",
    "region": "string"
  }
  ```
- **Response Format**:
  ```json
  {
    "recommendations": [
      {
        "title": "string",
        "release_date": "string"
      }
    ]
  }
  ```

### 5. `/get-recommendation-from-genre`
- **Request Type**: `POST`
- **Purpose**: Get movie recommendations based on genre.
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
        "release_date": "string"
      }
    ]
  }
  ```

### 6. `/get-random-recommendation`
- **Request Type**: `POST`
- **Purpose**: Get a random movie recommendation.
- **Request Format**:
  ```json
  {
    "region": "string"
  }
  ```
- **Response Format**:
  ```json
  {
    "recommendations": [
      {
        "title": "string",
        "release_date": "string"
      }
    ]
  }
  ```
  
### 7. `/Get-summery-of-movie`
- **Request Type**: `POST`
- **Purpose**: Get a movie summery.
- **Request Format**:
  ```json
  {
    "title": "string"
  }
  ```
- **Response Format**:
  ```json
  {
    "recommendations": [
      {
        "title": "string",
        "release_date": "string",
        "summery": "string",
      }
    ]
  }
  ```
### 8. `/Get-trending-movie`
- **Request Type**: `POST`
- **Purpose**: Get a trending movie.
- **Request Format**:
  ```json
  {

  }
  ```
- **Response Format**:
  ```json
  {
    "recommendations": [
      {
        "title": "string",
        "release_date": "string",
      }
    ]
  }
  ```
