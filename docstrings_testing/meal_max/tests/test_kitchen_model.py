import pytest
import sqlite3
from meal_max.models.kitchen_model import (
    create_meal,
    clear_meals,
    delete_meal,
    get_leaderboard,
    get_meal_by_id,
    get_meal_by_name,
    update_meal_stats,
    Meal
)
from meal_max.utils.sql_utils import get_db_connection


@pytest.fixture(scope='module')
def setup_database():
    """Set up the test database before tests."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE meals (
            id INTEGER PRIMARY KEY,
            meal TEXT UNIQUE NOT NULL,
            cuisine TEXT NOT NULL,
            price REAL NOT NULL,
            difficulty TEXT NOT NULL CHECK (difficulty IN ('LOW', 'MED', 'HIGH')),
            battles INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            deleted BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    yield
    conn.close()


@pytest.fixture
def meal_data():
    return {
        "meal": "Spaghetti Bolognese",
        "cuisine": "Italian",
        "price": 12.99,
        "difficulty": "MED"
    }


def test_create_meal(setup_database, meal_data):
    """Test creating a meal."""
    create_meal(**meal_data)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meals WHERE meal = ?", (meal_data['meal'],))
        meal = cursor.fetchone()
    assert meal is not None
    assert meal[1] == meal_data['meal']


def test_create_meal_duplicate(setup_database, meal_data):
    """Test creating a meal with a duplicate name."""
    create_meal(**meal_data)
    with pytest.raises(ValueError, match="Meal with name 'Spaghetti Bolognese' already exists"):
        create_meal(**meal_data)


def test_create_meal_invalid_price(setup_database):
    """Test creating a meal with an invalid price."""
    with pytest.raises(ValueError, match="Invalid price: -10.0. Price must be a positive number."):
        create_meal("Salad", "Healthy", -10.0, "LOW")


def test_create_meal_invalid_difficulty(setup_database):
    """Test creating a meal with an invalid difficulty."""
    with pytest.raises(ValueError, match="Invalid difficulty level: 'EXTRA'. Must be 'LOW', 'MED', or 'HIGH'."):
        create_meal("Pasta", "Italian", 15.0, "EXTRA")


def test_get_meal_by_id(setup_database, meal_data):
    """Test retrieving a meal by ID."""
    create_meal(**meal_data)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM meals WHERE meal = ?", (meal_data['meal'],))
        meal_id = cursor.fetchone()[0]
    meal = get_meal_by_id(meal_id)
    assert meal.id == meal_id
    assert meal.meal == meal_data['meal']


def test_get_meal_by_id_not_found(setup_database):
    """Test retrieving a meal that does not exist."""
    with pytest.raises(ValueError, match="Meal with ID 999 not found"):
        get_meal_by_id(999)


def test_get_meal_by_name(setup_database, meal_data):
    """Test retrieving a meal by name."""
    create_meal(**meal_data)
    meal = get_meal_by_name(meal_data['meal'])
    assert meal.meal == meal_data['meal']


def test_get_meal_by_name_not_found(setup_database):
    """Test retrieving a meal by name that does not exist."""
    with pytest.raises(ValueError, match="Meal with name 'Nonexistent Meal' not found"):
        get_meal_by_name("Nonexistent Meal")


def test_delete_meal(setup_database, meal_data):
    """Test deleting a meal."""
    create_meal(**meal_data)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM meals WHERE meal = ?", (meal_data['meal'],))
        meal_id = cursor.fetchone()[0]
    delete_meal(meal_id)
    with pytest.raises(ValueError, match=f"Meal with ID {meal_id} has been deleted"):
        get_meal_by_id(meal_id)


def test_clear_meals(setup_database, meal_data):
    """Test clearing all meals."""
    create_meal(**meal_data)
    clear_meals()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meals")
        meals = cursor.fetchall()
    assert len(meals) == 0


def test_update_meal_stats(setup_database, meal_data):
    """Test updating meal statistics."""
    create_meal(**meal_data)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM meals WHERE meal = ?", (meal_data['meal'],))
        meal_id = cursor.fetchone()[0]
    update_meal_stats(meal_id, "win")
    meal = get_meal_by_id(meal_id)
    assert meal.battles == 1
    assert meal.wins == 1
    update_meal_stats(meal_id, "loss")
    meal = get_meal_by_id(meal_id)
    assert meal.battles == 2
    assert meal.wins == 1


def test_get_leaderboard(setup_database):
    """Test getting the leaderboard."""
    create_meal("Meal A", "Cuisine A", 10.0, "LOW")
    create_meal("Meal B", "Cuisine B", 20.0, "MED")
    create_meal("Meal C", "Cuisine C", 15.0, "HIGH")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM meals WHERE meal = 'Meal A'")
        meal_a_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM meals WHERE meal = 'Meal B'")
        meal_b_id = cursor.fetchone()[0]
    
    update_meal_stats(meal_a_id, "win")
    update_meal_stats(meal_b_id, "win")
    update_meal_stats(meal_b_id, "loss")
    
    leaderboard = get_leaderboard(sort_by="wins")
    assert leaderboard[0]['meal'] == "Meal B"
    assert leaderboard[1]['meal'] == "Meal A"


if __name__ == "__main__":
    pytest.main()
