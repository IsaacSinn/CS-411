'''
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

  '''


import requests
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access the variables
TMDB_KEY = os.getenv("TMDB_KEY")

def _get_genre_id(genre_name):
    """Fetch the genre ID for a given genre name."""
    url = f"https://api.themoviedb.org/3/genre/movie/list"
    params = {
        "api_key": TMDB_KEY,
        "language": "en-US"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    genres = response.json()["genres"]
    for genre in genres:
        if genre["name"].lower() == genre_name.lower():
            return genre["id"]

    raise ValueError(f"Genre '{genre_name}' not found!")


def get_recommendations_for_genre(genre_name):
    """Fetch recommended movies for a specific genre."""

    # call _get_genre_id to get the genre id
    genre_id = _get_genre_id(genre_name)



    url = f"https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": TMDB_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "with_genres": genre_id,
        "page": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    movies = response.json()["results"]
    return [movie["title"] for movie in movies]

def get_recommendations_from_movie(movie_name):
    """Fetch recommended movies based on another movie."""
    search_url = f"https://api.themoviedb.org/3/search/movie"
    search_params = {
        "api_key": TMDB_KEY,
        "query": movie_name,
        "language": "en-US"
    }
    search_response = requests.get(search_url, params=search_params)
    search_response.raise_for_status()

    results = search_response.json()["results"]
    if not results:
        raise ValueError(f"Movie '{movie_name}' not found!")

    movie_id = results[0]["id"]

    recommendations_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
    recommendations_params = {
        "api_key": TMDB_KEY,
        "language": "en-US"
    }
    recommendations_response = requests.get(recommendations_url, params=recommendations_params)
    recommendations_response.raise_for_status()

    recommended_movies = recommendations_response.json()["results"]
    return [movie["title"] for movie in recommended_movies]

def get_random_recommendation():
    """Fetch a random movie recommendation."""
    url = f"https://api.themoviedb.org/3/movie/popular"
    params = {
        "api_key": TMDB_KEY,
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    movies = response.json()["results"]
    return [movie["title"] for movie in movies]

def get_movie_summary(movie_name):
    """Fetch the summary of a movie."""
    search_url = f"https://api.themoviedb.org/3/search/movie"
    search_params = {
        "api_key": TMDB_KEY,
        "query": movie_name,
        "language": "en-US"
    }
    search_response = requests.get(search_url, params=search_params)
    search_response.raise_for_status()

    results = search_response.json()["results"]
    if not results:
        raise ValueError(f"Movie '{movie_name}' not found!")

    movie_id = results[0]["id"]

    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    movie_params = {
        "api_key": TMDB_KEY,
        "language": "en-US"
    }
    movie_response = requests.get(movie_url, params=movie_params)
    movie_response.raise_for_status()

    movie = movie_response.json()
    return movie["overview"]

def get_trending_movies_tmdb():
    """Fetch the trending movie."""
    url = f"https://api.themoviedb.org/3/trending/movie/week"
    params = {
        "api_key": TMDB_KEY,
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    movies = response.json()["results"]
    print("retreived movies")
    return [movie["title"] for movie in movies]

if __name__ == "__main__":
    
    # Unit test for get_recommendations function
    print("\n ###### Unit test for get_recommendations function ###### \n")

    genre_name = "comedy"
    recommendations = get_recommendations_for_genre(genre_name)

    print(f"Recommendations for {genre_name}:")

    for i, movie in enumerate(recommendations, start=1):
        print(f"{i}. {movie}")


    # Unit test for get_movie_recommendations function
    print("\n ###### Unit test for get_movie_recommendations function ###### \n")
    movie_name = "The Dark Knight"
    recommendations = get_recommendations_from_movie(movie_name)

    print(f"Recommendations for {movie_name}:")
    for i, movie in enumerate(recommendations, start=1):
        print(f"{i}. {movie}")

    # Unit test for get_random_recommendation function
    print("\n ###### Unit test for get_random_recommendation function ###### \n")
    recommendations = get_random_recommendation()

    print("Random recommendations:")
    for i, movie in enumerate(recommendations, start=1):
        print(f"{i}. {movie}")

    # Unit test for get_movie_summary function
    print("\n ###### Unit test for get_movie_summary function ###### \n")
    movie_name = "The Dark Knight"
    summary = get_movie_summary(movie_name)

    print(f"Summary for {movie_name}:")
    
    print(summary)

    # Unit test for get_trending_movie function
    print("\n ###### Unit test for get_trending_movie function ###### \n")
    recommendations = get_trending_movies_tmdb()

    print("Trending movies:")

    for i, movie in enumerate(recommendations, start=1):
        print(f"{i}. {movie}")
