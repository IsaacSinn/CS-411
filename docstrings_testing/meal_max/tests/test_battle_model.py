import pytest
from unittest.mock import patch
from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal
from meal_max.utils.random_utils import get_random


@pytest.fixture
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()


@pytest.fixture
def combatant_1():
    """Fixture for a sample Meal object representing combatant 1."""
    return Meal(id=1, meal="Pasta", price=10.0, cuisine="Italian", difficulty="MED")


@pytest.fixture
def combatant_2():
    """Fixture for a sample Meal object representing combatant 2."""
    return Meal(id=2, meal="Sushi", price=15.0, cuisine="Japanese", difficulty="HIGH")


##################################################
# Battle Method Test Cases
##################################################

def test_battle_success(battle_model, combatant_1, combatant_2):
    """Test battle between two combatants and check that the winner's name is returned."""
    battle_model.prep_combatant(combatant_1)
    battle_model.prep_combatant(combatant_2)

    with patch("meal_max.models.battle_model.get_random", return_value=0.5):
        with patch("meal_max.models.battle_model.update_meal_stats") as mock_update:
            winner_name = battle_model.battle()
            assert winner_name in {combatant_1.meal, combatant_2.meal}, "Winner should be one of the combatants' names"
            mock_update.assert_any_call(combatant_1.id, 'win')
            mock_update.assert_any_call(combatant_2.id, 'loss')
            assert len(battle_model.combatants) == 1, "One combatant should remain after the battle"


def test_battle_not_enough_combatants(battle_model, combatant_1):
    """Test battle raises ValueError when there are fewer than two combatants."""
    battle_model.prep_combatant(combatant_1)
    
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()


##################################################
# Combatant Management Test Cases
##################################################

def test_prep_combatant_success(battle_model, combatant_1, combatant_2):
    """Test adding combatants to the battle."""
    battle_model.prep_combatant(combatant_1)
    battle_model.prep_combatant(combatant_2)

    assert len(battle_model.combatants) == 2, "Two combatants should be prepped for battle"


def test_prep_combatant_list_full(battle_model, combatant_1, combatant_2):
    """Test error when attempting to add more than two combatants."""
    battle_model.prep_combatant(combatant_1)
    battle_model.prep_combatant(combatant_2)
    
    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(combatant_1)  # Attempting to add a third combatant


def test_clear_combatants(battle_model, combatant_1, combatant_2):
    """Test clearing the combatants list."""
    battle_model.prep_combatant(combatant_1)
    battle_model.prep_combatant(combatant_2)
    battle_model.clear_combatants()

    assert len(battle_model.combatants) == 0, "Combatants list should be empty after clearing"


##################################################
# Battle Score Calculation Test Cases
##################################################

def test_get_battle_score(battle_model, combatant_1):
    """Test battle score calculation for a given combatant."""
    expected_score = (combatant_1.price * len(combatant_1.cuisine)) - 2  # MED difficulty modifier
    calculated_score = battle_model.get_battle_score(combatant_1)

    assert calculated_score == expected_score, f"Expected score {expected_score}, got {calculated_score}"


##################################################
# Random Number Dependent Outcome Test Cases
##################################################

def test_battle_with_random_number_favor_combatant_1(battle_model, combatant_1, combatant_2):
    """Test battle outcome when random number favors combatant 1."""
    battle_model.prep_combatant(combatant_1)
    battle_model.prep_combatant(combatant_2)

    with patch("meal_max.models.battle_model.get_random", return_value=0.9):
        winner_name = battle_model.battle()
        assert winner_name == combatant_1.meal, "Combatant 1 should win with high random number"


def test_battle_with_random_number_favor_combatant_2(battle_model, combatant_1, combatant_2):
    """Test battle outcome when random number favors combatant 2."""
    battle_model.prep_combatant(combatant_1)
    battle_model.prep_combatant(combatant_2)

    with patch("meal_max.models.battle_model.get_random", return_value=0.1):
        winner_name = battle_model.battle()
        assert winner_name == combatant_2.meal, "Combatant 2 should win with low random number"


##################################################
# Combatants Retrieval Test Cases
##################################################

def test_get_combatants(battle_model, combatant_1, combatant_2):
    """Test retrieving the current list of combatants."""
    battle_model.prep_combatant(combatant_1)
    battle_model.prep_combatant(combatant_2)
    
    combatants = battle_model.get_combatants()
    assert combatants == [combatant_1, combatant_2], "Combatants should match those prepped for battle"
