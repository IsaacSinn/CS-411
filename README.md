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
