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

# Fixtures

def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()

# Mocking the database connection for tests
@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None

    @contextmanager
    def mock_get_db_connection():
        yield mock_conn

    mocker.patch("meal_max.models.kitchen_model.get_db_connection", mock_get_db_connection)

    return mock_cursor

# Add, Delete, and Retrieve Meals

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

def test_clear_meals(mock_cursor, mocker):
    """Test clearing all meals from the meals table."""
    mocker.patch.dict('os.environ', {'SQL_CREATE_TABLE_PATH': 'sql/create_meal_table.sql'})
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="SQL script to recreate the meals table"))

    clear_meals()

    mock_open.assert_called_once_with('sql/create_meal_table.sql', 'r')
    mock_cursor.executescript.assert_called_once_with("SQL script to recreate the meals table")


def test_get_meal_by_name(mock_cursor):
    """Test retrieving a meal by its name."""
    mock_cursor.fetchone.return_value = (1, "Pasta", "Italian", 12.5, "MED", False)

    meal = get_meal_by_name("Pasta")

    expected_meal = Meal(id=1, meal="Pasta", cuisine="Italian", price=12.5, difficulty="MED")
    assert meal == expected_meal, f"Expected {expected_meal}, but got {meal}"

    expected_query = "SELECT id, meal, cuisine, price, difficulty, deleted FROM meals WHERE meal = ?"
    actual_query = mock_cursor.execute.call_args[0][0].strip()
    assert expected_query.strip() == actual_query

    expected_args = ("Pasta",)
    actual_args = mock_cursor.execute.call_args[0][1]
    assert expected_args == actual_args, f"Expected arguments {expected_args}, got {actual_args}"

def test_get_meal_by_name_not_found(mock_cursor):
    """Test retrieving a meal by its name that does not exist."""
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="Meal with name Pasta not found"):
        get_meal_by_name("Pasta")


def test_get_leaderboard(mock_cursor):
    """Test retrieving a leaderboard of meals sorted by wins."""
    mock_cursor.fetchall.return_value = [
        (1, "Pasta", "Italian", 12.5, "MED", 10, 7, 70),
        (2, "Pizza", "Italian", 15.0, "LOW", 20, 12, 60),
        (3, "Sushi", "Japanese", 25.0, "HIGH", 5, 3, 60)
    ]

    leaderboard = get_leaderboard(sort_by="wins")

    expected_result = [
        {'id': 1, 'meal': "Pasta", 'cuisine': "Italian", 'price': 12.5, 'difficulty': "MED", 'battles': 10, 'wins': 7, 'win_pct': round(70 * 100, 1)},
        {'id': 2, 'meal': "Pizza", 'cuisine': "Italian", 'price': 15.0, 'difficulty': "LOW", 'battles': 20, 'wins': 12, 'win_pct': round(60 * 100, 1)},
        {'id': 3, 'meal': "Sushi", 'cuisine': "Japanese", 'price': 25.0, 'difficulty': "HIGH", 'battles': 5, 'wins': 3, 'win_pct': round(60 * 100, 1)}
    ]
    assert leaderboard == expected_result, f"Expected {expected_result}, but got {leaderboard}"

    expected_query = """
        SELECT id, meal, cuisine, price, difficulty, battles, wins, (wins * 1.0 / battles) AS win_pct
        FROM meals WHERE deleted = false AND battles > 0
        ORDER BY wins DESC
    """
    actual_query = mock_cursor.execute.call_args[0][0].strip()
    assert normalize_whitespace(expected_query) == normalize_whitespace(actual_query)
