from models.tmdb_model import *


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