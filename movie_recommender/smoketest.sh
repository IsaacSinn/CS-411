#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000"

# Flag to control whether to echo JSON output
ECHO_JSON=true

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health-check" | grep -q '"status": "ok"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

##############################################
#
# User management
#
##############################################

# Function to create a user
create_account() {
  echo "Creating a new user account..."
  response=$(curl -s -X POST "$BASE_URL/create-account" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  
  if echo "$response" | grep -q '"message": "Account created successfully."'; then
    echo "User account created successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Create Account Response JSON:"
      echo "$response" | jq .
    fi
  elif echo "$response" | grep -q '"error": "Username already exists."'; then
    echo "Username already exists. Skipping account creation."
    if [ "$ECHO_JSON" = true ]; then
      echo "Create Account Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to create user account."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}


# Function to log in a user
login_user() {
  echo "Logging in user..."
  response=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if echo "$response" | grep -q '"message": "Login successful."'; then
    echo "User logged in successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Login Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to log in user."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

update_password() {
  echo "Updating password..."
  response=$(curl -s -X POST "$BASE_URL/update-password" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "old_password":"password123", "new_password":"newpassword123"}')
  if echo "$response" | grep -q '"message": "Password updated successfully."'; then
    echo "Password updated successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Update Password Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to update password."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

delete_user() {
  echo "Deleting user account..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-user" -H "Content-Type: application/json" \
    -d '{"username":"testuser"}')
  
  if echo "$response" | grep -q '"status": "user deleted"'; then
    echo "User account deleted successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Delete User Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to delete user account."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

###############################################
#
# Get recommendation from movies
#
###############################################

get_recommendation_from_movies() {
  echo "Getting movie recommendations based on other movies..."
  response=$(curl -s -X POST "$BASE_URL/get-recommendation-from-movies" -H "Content-Type: application/json" \
    -d '{"title":"Inception", "region":"US"}')
  if echo "$response" | jq -e '.recommendations | length > 0' > /dev/null; then
    echo "Movie recommendations retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Recommendations Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve movie recommendations."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

get_recommendation_from_genre() {
  echo "Getting movie recommendations based on genre..."
  response=$(curl -s -X POST "$BASE_URL/get-recommendation-from-genre" -H "Content-Type: application/json" \
    -d '{"genre":"Action", "region":"US"}')
  if echo "$response" | jq -e '.recommendations | length > 0' > /dev/null; then
    echo "Genre-based recommendations retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Recommendations Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve genre-based recommendations."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

get_random_recommendation() {
  echo "Getting a random movie recommendation..."
  response=$(curl -s -X POST "$BASE_URL/get-random-recommendation" -H "Content-Type: application/json" \
    -d '{"region":"US"}')
  if echo "$response" | jq -e '.recommendations | length > 0' > /dev/null; then
    echo "Random movie recommendation retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Random Recommendation Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve a random movie recommendation."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

get_trending_movie() {
  echo "Getting trending movie..."
  response=$(curl -s -X POST "$BASE_URL/get-trending-movies" -H "Content-Type: application/json" -d '{"region":"US"}')
  if echo "$response" | grep -q '"status": "ok"'; then
    echo "Trending movie retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Trending Movie Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve trending movie."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

###############################################
#
# Get summary of movie
#
###############################################

get_summary_of_movie() {
  echo "Getting summary of a movie..."
  response=$(curl -s -X POST "$BASE_URL/get-movie-summary" -H "Content-Type: application/json" \
    -d '{"title":"Inception"}')
  if echo "$response" | grep -q '"status": "ok"'; then
    echo "Movie summary retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Movie Summary Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve movie summary."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

# Run all the steps in order
check_health
create_account
login_user
update_password
delete_user
get_recommendation_from_movies
get_recommendation_from_genre
get_random_recommendation
get_trending_movie
get_summary_of_movie
