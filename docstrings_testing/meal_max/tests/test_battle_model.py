import pytest
from meal_max.models.kitchen_model import Meal
from meal_max.models.battle_model import BattleModel

@pytest.fixture
def battle_model():
    """Fixture to create a BattleModel instance for testing."""
    return BattleModel()

@pytest.fixture
def meal_1():
    """Fixture to create a sample meal for testing."""
    return Meal(id=1, meal="Meal 1", price=10.0, cuisine="Italian", difficulty="HIGH")

@pytest.fixture
def meal_2():
    """Fixture to create another sample meal for testing."""
    return Meal(id=2, meal="Meal 2", price=15.0, cuisine="Chinese", difficulty="MED")

def test_battle_no_combatants(battle_model):
    """Test that ValueError is raised when there are fewer than two combatants."""
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()

def test_battle_with_one_combatant(battle_model, meal_1):
    """Test that ValueError is raised when there is only one combatant."""
    battle_model.prep_combatant(meal_1)
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()

def test_battle_success(battle_model, meal_1, meal_2, mocker):
    """Test that the battle method returns the correct winner."""
    # Mock get_random to return a fixed number for testing
    mock_random = mocker.patch('meal_max.utils.random_utils.get_random', return_value=0.5)
    
    # Mock update_meal_stats
    mock_update_stats = mocker.patch('meal_max.models.kitchen_model.update_meal_stats')
    
    battle_model.prep_combatant(meal_1)
    battle_model.prep_combatant(meal_2)

    winner = battle_model.battle()
    
    assert winner in [meal_1.meal, meal_2.meal]
    mock_random.assert_called_once()
    mock_update_stats.assert_any_call(meal_1.id, 'win') or mock_update_stats.assert_any_call(meal_2.id, 'win')

def test_clear_combatants(battle_model, meal_1, meal_2):
    """Test that the clear_combatants method clears the combatants list."""
    battle_model.prep_combatant(meal_1)
    battle_model.prep_combatant(meal_2)
    assert len(battle_model.get_combatants()) == 2

    battle_model.clear_combatants()
    assert len(battle_model.get_combatants()) == 0

def test_get_battle_score(battle_model, meal_1):
    """Test that get_battle_score calculates the correct score."""
    score = battle_model.get_battle_score(meal_1)
    expected_score = (meal_1.price * len(meal_1.cuisine)) - 1  # difficulty HIGH corresponds to -1
    assert score == expected_score

def test_get_combatants(battle_model, meal_1, meal_2):
    """Test that get_combatants returns the correct list of combatants."""
    battle_model.prep_combatant(meal_1)
    battle_model.prep_combatant(meal_2)

    combatants = battle_model.get_combatants()
    assert len(combatants) == 2
    assert combatants[0].meal == meal_1.meal
    assert combatants[1].meal == meal_2.meal

def test_prep_combatant_full_list(battle_model, meal_1, meal_2):
    """Test that ValueError is raised when trying to add a third combatant."""
    battle_model.prep_combatant(meal_1)
    battle_model.prep_combatant(meal_2)

    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(Meal(id=3, meal="Meal 3", price=12.0, cuisine="Mexican", difficulty="LOW"))