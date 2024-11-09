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

create_meal() {
  meal=$1
  cuisine=$2
  price=$3
  difficulty=$4

  echo "Creating meal: $meal, Cuisine: $cuisine, Price: $price, Difficulty: $difficulty..."
  response=$(curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d "{\"meal\":\"$meal\", \"cuisine\":\"$cuisine\", \"price\":$price, \"difficulty\":\"$difficulty\"}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal created successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to create meal."
    exit 1
  fi
}

delete_meal() {
  meal_id=$1

  echo "Deleting meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal deleted successfully."
  else
    echo "Failed to delete meal."
    exit 1
  fi
}

get_meal_by_id() {
  meal_id=$1

  echo "Retrieving meal by ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve meal by ID."
    exit 1
  fi
}

get_meal_by_name() {
  meal_name=$1

  echo "Retrieving meal by name ($meal_name)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-name/$meal_name")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve meal by name."
    exit 1
  fi
}

get_leaderboard() {
  echo "Retrieving meal leaderboard..."
  response=$(curl -s -X GET "$BASE_URL/get-leaderboard?sort_by=wins")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve leaderboard."
    exit 1
  fi
}

update_meal_stats() {
  meal_id=$1
  result=$2

  echo "Updating meal stats for ID ($meal_id) with result ($result)..."
  response=$(curl -s -X POST "$BASE_URL/update-meal-stats" -H "Content-Type: application/json" \
    -d "{\"meal_id\":$meal_id, \"result\":\"$result\"}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal stats updated successfully."
  else
    echo "Failed to update meal stats."
    exit 1
  fi
}

##########################################################
#
# Battle Management
#
##########################################################

prep_combatant() {
  meal_id=$1
  
  echo "Preparing combatant with meal ID ($meal_id)..."
  response=$(curl -s -X POST "$BASE_URL/prep-combatant/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Combatant prepared successfully."
  else
    echo "Failed to prepare combatant."
    exit 1
  fi
}

battle() {
  echo "Conducting battle between meals..."
  response=$(curl -s -X POST "$BASE_URL/battle")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Battle conducted successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to conduct battle."
    exit 1
  fi
}

get_battle_score() {
  meal_id=$1

  echo "Getting battle score for meal ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-battle-score/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Battle score retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to get battle score."
    exit 1
  fi
}

clear_combatants() {
  echo "Clearing combatants..."
  response=$(curl -s -X POST "$BASE_URL/clear-combatants")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Combatants cleared successfully."
  else
    echo "Failed to clear combatants."
    exit 1
  fi
}

get_combatants() {
  echo "Retrieving current combatants..."
  response=$(curl -s -X GET "$BASE_URL/get-combatants")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Combatants retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve combatants."
    exit 1
  fi
}

##########################################################
#
# Random Number Generation
#
##########################################################

get_random_number() {
  echo "Fetching a random number..."
  response=$(curl -s -X GET "$BASE_URL/get-random")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Random number retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to fetch random number."
    exit 1
  fi
}


# Health checks
check_health
check_db

# Meal Management Tests
create_meal "Spaghetti" "Italian" 12.99 "MED"
create_meal "Sushi" "Japanese" 19.99 "HIGH"
create_meal "Tacos" "Mexican" 8.99 "LOW"

get_meal_by_id 1
get_meal_by_name "Sushi"
get_leaderboard

# Update stats for meals
update_meal_stats 1 "win"
update_meal_stats 2 "loss"

delete_meal 3  # Delete Tacos
get_meal_by_id 3  # This should fail as the meal is deleted

# Battle Management Tests
prep_combatant 1  # Prepare the first meal
prep_combatant 2  # Prepare the second meal
battle_meals  # Ensure that two meals are ready for battle

# Random Number Test
get_random_number

echo "All tests passed successfully!"
