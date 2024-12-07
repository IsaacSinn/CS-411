# Movie Recommendation System

## Overview
The Movie Recommendation System is a web application designed to provide personalized movie recommendations, allow users to search for movies, and maintain a personal watchlist. This project utilizes Flask for the backend, SQLite for data storage, and the TMDB (The Movie Database) API for movie data.

## How to run it
Navigate to the directory containing Dockerfile
```bash
docker build -t flask-app .
```
Once the image is built, you can run a container using the following command:
```bash
docker run -d -p 5000:5000 --name flask-container flask-app
```

## Testing Changes

If you make changes to the application code, follow these steps:

1. **Stop the container:**
  ```bash
  docker stop flask-container
  ```
2. **Remove the container:**
  ```bash
  docker rm flask-container
  ```
3. **Rebuild the image and run the new container**


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
