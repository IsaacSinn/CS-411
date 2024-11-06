import pytest
from meal_max.models.kitchen_model import Meal
from meal_max.models.battle_model import BattleModel
from meal_max.utils.random_utils import get_random
from meal_max.models.kitchen_model import update_meal_stats


class TestBattleModel:
    @pytest.fixture
    def battle_model(self):
        return BattleModel()

    @pytest.fixture
    def meal_1(self):
        return Meal(id=1, meal="Meal A", price=15.0, cuisine="Italian", difficulty="MED")

    @pytest.fixture
    def meal_2(self):
        return Meal(id=2, meal="Meal B", price=12.0, cuisine="Mexican", difficulty="HIGH")
    
    @pytest.fixture
    def mock_update_meal_stats(self, mocker):
        """Mock the update_meal_stats function for testing purposes."""
        return mocker.patch("meal_max.models.battle_model.update_meal_stats")

    def test_prep_combatant(self, battle_model, meal_1, meal_2):
        battle_model.prep_combatant(meal_1)
        battle_model.prep_combatant(meal_2)
        combatants = battle_model.get_combatants()
        assert len(combatants) == 2
        assert combatants[0].meal == "Meal A"
        assert combatants[1].meal == "Meal B"

    def test_prep_combatant_max_limit(self, battle_model, meal_1, meal_2):
        battle_model.prep_combatant(meal_1)
        battle_model.prep_combatant(meal_2)
        with pytest.raises(ValueError):
            battle_model.prep_combatant(Meal(id=3, meal="Meal C", price=10.0, cuisine="French", difficulty="LOW"))

    def test_battle(self, battle_model, meal_1, meal_2, mock_update_meal_stats):
        battle_model.prep_combatant(meal_1)
        battle_model.prep_combatant(meal_2)
        
        winner_name = battle_model.battle()
        
        assert winner_name in ["Meal A", "Meal B"]
        mock_update_meal_stats.assert_called_with(
            meal_1.id if winner_name == "Meal A" else meal_2.id,
            "win"
        )
        mock_update_meal_stats.assert_called_with(
            meal_2.id if winner_name == "Meal A" else meal_1.id,
            "loss"
        )
        assert len(battle_model.get_combatants()) == 1

    def test_battle_not_enough_combatants(self, battle_model, meal_1):
        battle_model.prep_combatant(meal_1)
        with pytest.raises(ValueError):
            battle_model.battle()

    def test_clear_combatants(self, battle_model, meal_1, meal_2):
        battle_model.prep_combatant(meal_1)
        battle_model.prep_combatant(meal_2)
        battle_model.clear_combatants()
        assert battle_model.get_combatants() == []

    def test_get_battle_score(self, battle_model, meal_1, meal_2):
        score_1 = battle_model.get_battle_score(meal_1)
        score_2 = battle_model.get_battle_score(meal_2)
        
        # The actual score depends on the specifics of the meal attributes
        assert isinstance(score_1, float)
        assert isinstance(score_2, float)
        assert score_1 != score_2  # Assumes differing attributes between meal_1 and meal_2

    def test_battle_winner_determined_by_random(self, battle_model, meal_1, meal_2, mock_update_meal_stats):

        battle_model.prep_combatant(meal_1)
        battle_model.prep_combatant(meal_2)
        
        winner_name = battle_model.battle()
        
        assert winner_name == meal_1.meal
        mock_update_meal_stats.assert_called_with(meal_2.id, "win")
        mock_update_meal_stats.assert_called_with(meal_1.id, "loss")
