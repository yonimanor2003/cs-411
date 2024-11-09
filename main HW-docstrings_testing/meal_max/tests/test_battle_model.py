import pytest
from meal_max.models.kitchen_model import Meal
from meal_max.models.battle_model import BattleModel


@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

@pytest.fixture()
def sample_meal1():
    """Creates a sample Meal object for testing."""
    return Meal(id=1, meal='Meal 1', cuisine='Cuisine 1', price=10.0, difficulty='MED')

@pytest.fixture()
def sample_meal2():
    """Creates another sample Meal object for testing."""
    return Meal(id=2, meal='Meal 2', cuisine='Cuisine 2', price=15.0, difficulty='HIGH')

@pytest.fixture()
def sample_meal3():
    """Creates another sample Meal object for testing."""
    return Meal(id=3, meal='Meal 3', cuisine='Cuisine 3', price=12.0, difficulty='LOW')


##################################################
# Combatant Management Test Cases
##################################################

def test_prep_combatant(battle_model, sample_meal1):
    """Test preparing a combatant for battle."""
    battle_model.prep_combatant(sample_meal1)
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0].meal == 'Meal 1'


def test_prep_two_combatants(battle_model, sample_meal1, sample_meal2):
    """Test preparing two combatants for battle."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    assert len(battle_model.combatants) == 2


def test_prep_more_than_two_combatants(battle_model, sample_meal1, sample_meal2, sample_meal3):
    """Test error when trying to prepare a third combatant."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    with pytest.raises(ValueError, match="Combatant list is full"):
        battle_model.prep_combatant(sample_meal3)


def test_clear_combatants(battle_model, sample_meal1, sample_meal2):
    """Test clearing the list of combatants."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    battle_model.clear_combatants()
    assert len(battle_model.combatants) == 0


##################################################
# Battle Management Test Cases
##################################################

def test_battle(battle_model, sample_meal1, sample_meal2, mocker):
    """Test conducting a battle between two combatants."""
    # Mock the update_meal_stats function to avoid side effects during testing
    mock_update_meal_stats = mocker.patch("meal_max.models.battle_model.update_meal_stats")
    
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)

    winner = battle_model.battle()
    
    # Assert that one of the meals is the winner
    assert winner in ['Meal 1', 'Meal 2']

    # Assert that update_meal_stats was called twice for win and loss
    assert mock_update_meal_stats.call_count == 2


def test_battle_not_enough_combatants(battle_model):
    """Test error when not enough combatants are present for a battle."""
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()


##################################################
# Score Calculation Test Cases
##################################################

def test_get_battle_score(battle_model, sample_meal1):
    """Test calculating the battle score for a combatant."""
    battle_model.prep_combatant(sample_meal1)
    score = battle_model.get_battle_score(sample_meal1)
    assert score == (sample_meal1.price * len(sample_meal1.cuisine)) - 2  # Difficulty is 'MED', so modifier is 2

def test_get_battle_score_low_difficulty(battle_model, sample_meal3):
    """Test calculating the battle score for a combatant with low difficulty."""
    battle_model.prep_combatant(sample_meal3)
    score = battle_model.get_battle_score(sample_meal3)
    assert score == (sample_meal3.price * len(sample_meal3.cuisine)) - 3  # Difficulty is 'LOW', so modifier is 3


def test_get_battle_score_high_difficulty(battle_model, sample_meal2):
    """Test calculating the battle score for a combatant with high difficulty."""
    battle_model.prep_combatant(sample_meal2)
    score = battle_model.get_battle_score(sample_meal2)
    assert score == (sample_meal2.price * len(sample_meal2.cuisine)) - 1  # Difficulty is 'HIGH', so modifier is 1
