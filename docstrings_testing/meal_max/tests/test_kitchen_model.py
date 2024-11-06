import pytest
from contextlib import contextmanager
import sqlite3
from meal_max.models.kitchen_model import (
    Meal,
    create_meal,
    clear_meals,
    delete_meal,
    get_meal_by_id,
    get_meal_by_name,
    update_meal_stats,
    get_leaderboard
)
import re

######################################################
#
#    Fixtures
#
######################################################

def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()

# Mocking the database connection for tests
@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None

    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object

    mocker.patch("meal_max.models.kitchen_model.get_db_connection", mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test

######################################################
#
#    Add, Delete, and Retrieve Meals
#
######################################################

def test_create_meal(mock_cursor):
    """Test creating a new meal in the database."""
    create_meal(meal="Pasta", cuisine="Italian", price=12.5, difficulty="MED")

    expected_query = normalize_whitespace("""
        INSERT INTO meals (meal, cuisine, price, difficulty)
        VALUES (?, ?, ?, ?)
    """)

    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert expected_query.strip() == actual_query, "The SQL query did not match the expected structure."

    expected_args = ("Pasta", "Italian", 12.5, "MED")
    actual_args = mock_cursor.execute.call_args[0][1]
    assert expected_args == actual_args, f"The SQL query arguments did not match. Expected {expected_args}, got {actual_args}."

def test_create_meal_invalid_price():
    """Test error when trying to create a meal with an invalid price."""
    with pytest.raises(ValueError, match="Invalid price: -10. Price must be a positive number."):
        create_meal(meal="Soup", cuisine="French", price=-10, difficulty="LOW")

def test_create_meal_invalid_difficulty():
    """Test error when trying to create a meal with an invalid difficulty level."""
    with pytest.raises(ValueError, match="Invalid difficulty level: EASY. Must be 'LOW', 'MED', or 'HIGH'."):
        create_meal(meal="Cake", cuisine="Dessert", price=5.0, difficulty="EASY")

def test_delete_meal(mock_cursor):
    """Test marking a meal as deleted."""
    # Simulate meal exists
    mock_cursor.fetchone.return_value = [False]
    delete_meal(1)

    expected_select = "SELECT deleted FROM meals WHERE id = ?"
    expected_update = "UPDATE meals SET deleted = TRUE WHERE id = ?"
    actual_select = mock_cursor.execute.call_args_list[0][0][0].strip()
    actual_update = mock_cursor.execute.call_args_list[1][0][0].strip()
    assert expected_select.strip() == actual_select
    assert expected_update.strip() == actual_update

def test_get_meal_by_id(mock_cursor):
    """Test retrieving a meal by ID."""
    mock_cursor.fetchone.return_value = (1, "Pasta", "Italian", 12.5, "MED", False)
    meal = get_meal_by_id(1)
    assert meal == Meal(id=1, meal="Pasta", cuisine="Italian", price=12.5, difficulty="MED")

def test_get_meal_by_id_not_found(mock_cursor):
    """Test retrieving a meal by ID that does not exist."""
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Meal with ID 999 not found"):
        get_meal_by_id(999)

def test_update_meal_stats_win(mock_cursor):
    """Test updating meal stats for a win."""
    mock_cursor.fetchone.return_value = [False]
    update_meal_stats(1, "win")
    expected_update = "UPDATE meals SET battles = battles + 1, wins = wins + 1 WHERE id = ?"
    actual_update = mock_cursor.execute.call_args_list[1][0][0].strip()
    assert expected_update.strip() == actual_update
