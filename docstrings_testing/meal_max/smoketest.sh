#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

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
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

##########################################################
#
# Meal Management
#
##########################################################

clear_meals() {
  echo "Clearing all meals..."
  curl -s -X DELETE "$BASE_URL/clear-meals" | grep -q '"status": "success"'
}

create_meal() {
  name=$1
  category=$2
  calories=$3
  protein=$4
  carbs=$5
  fats=$6

  echo "Adding meal ($name, Category: $category) to the database..."
  curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d "{\"name\":\"$name\", \"category\":\"$category\", \"calories\":$calories, \"protein\":$protein, \"carbs\":$carbs, \"fats\":$fats}" | grep -q '"status": "success"'

  if [ $? -eq 0 ]; then
    echo "Meal added successfully."
  else
    echo "Failed to add meal."
    exit 1
  fi
}

delete_meal_by_id() {
  meal_id=$1

  echo "Deleting meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal deleted successfully by ID ($meal_id)."
  else
    echo "Failed to delete meal by ID ($meal_id)."
    exit 1
  fi
}

get_all_meals() {
  echo "Getting all meals in the database..."
  response=$(curl -s -X GET "$BASE_URL/get-all-meals")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "All meals retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meals JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meals."
    exit 1
  fi
}

get_meal_by_id() {
  meal_id=$1

  echo "Getting meal by ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by ID ($meal_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (ID $meal_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by ID ($meal_id)."
    exit 1
  fi
}

get_meals_by_category() {
  category=$1

  echo "Getting meals by category ($category)..."
  response=$(curl -s -X GET "$BASE_URL/get-meals-by-category?category=$(echo $category | sed 's/ /%20/g')")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meals retrieved successfully by category."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meals JSON (by category):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meals by category."
    exit 1
  fi
}

get_random_meal() {
  echo "Getting a random meal from the database..."
  response=$(curl -s -X GET "$BASE_URL/get-random-meal")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Random meal retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Random Meal JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get a random meal."
    exit 1
  fi
}


############################################################
#
# Meal Nutritional Information
#
############################################################

get_meal_nutritional_info() {
  meal_id=$1
  echo "Getting nutritional information for meal ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-nutritional-info/$meal_id")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Nutritional information retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Nutritional Info JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve nutritional information."
    exit 1
  fi
}


# Health checks
check_health
check_db

# Clear the meal catalog
clear_meals

# Create meals
create_meal "Chicken Salad" "Lunch" 300 25 10 15
create_meal "Fruit Smoothie" "Breakfast" 200 5 30 2
create_meal "Pasta Bolognese" "Dinner" 450 20 40 10
create_meal "Greek Yogurt" "Snack" 150 10 15 5
create_meal "Oatmeal" "Breakfast" 250 8 40 4

delete_meal_by_id 1
get_all_meals

get_meal_by_id 2
get_meals_by_category "Breakfast"
get_random_meal

get_meal_nutritional_info 2

echo "All meal tests passed successfully!"