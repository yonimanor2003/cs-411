import pytest
from meal_max.models.kitchen_model import Meal, create_meal, delete_meal, get_meal_by_id, get_meal_by_name, update_meal_stats
from meal_max.utils.sql_utils import get_db_connection

@pytest.fixture()
def meal_data():
    """Fixture to provide data for creating a meal."""
    return {
        'meal': 'Test Meal',
        'cuisine': 'Test Cuisine',
        'price': 10.0,
        'difficulty': 'MED'
    }

@pytest.fixture()
def meal_instance(meal_data):
    """Fixture to provide an instance of Meal."""
    return Meal(id=1, **meal_data)

@pytest.fixture(autouse=True)
def setup_database():
    """Setup and teardown the database for testing."""
    # Code to create test database tables, if needed
    yield
    # Code to drop test database tables, if needed

##################################################
# Meal Creation Test Cases
##################################################

def test_create_meal(meal_data):
    """Test creating a new meal."""
    create_meal(**meal_data)
    
    # Fetch the meal from the database
    meal = get_meal_by_name(meal_data['meal'])
    assert meal.meal == meal_data['meal']
    assert meal.cuisine == meal_data['cuisine']
    assert meal.price == meal_data['price']
    assert meal.difficulty == meal_data['difficulty']

def test_create_meal_invalid_price():
    """Test creating a meal with an invalid price."""
    with pytest.raises(ValueError, match="Invalid price: -1. Price must be a positive number."):
        create_meal(meal='Test Meal', cuisine='Test Cuisine', price=-1, difficulty='MED')

def test_create_meal_invalid_difficulty():
    """Test creating a meal with an invalid difficulty level."""
    with pytest.raises(ValueError, match="Invalid difficulty level: INVALID. Must be 'LOW', 'MED', or 'HIGH'."):
        create_meal(meal='Test Meal', cuisine='Test Cuisine', price=10.0, difficulty='INVALID')

def test_create_duplicate_meal(meal_data):
    """Test error when creating a meal that already exists."""
    create_meal(**meal_data)
    with pytest.raises(ValueError, match="Meal with name 'Test Meal' already exists"):
        create_meal(**meal_data)

##################################################
# Meal Deletion Test Cases
##################################################

def test_delete_meal(meal_data):
    """Test soft deleting a meal."""
    create_meal(**meal_data)
    meal = get_meal_by_name(meal_data['meal'])
    delete_meal(meal.id)

    with pytest.raises(ValueError, match=f"Meal with ID {meal.id} has been deleted"):
        get_meal_by_id(meal.id)

def test_delete_non_existent_meal():
    """Test error when attempting to delete a non-existent meal."""
    with pytest.raises(ValueError, match="Meal with ID 999 not found"):
        delete_meal(999)

def test_delete_already_deleted_meal(meal_data):
    """Test error when attempting to delete a meal that has already been deleted."""
    create_meal(**meal_data)
    meal = get_meal_by_name(meal_data['meal'])
    delete_meal(meal.id)

    with pytest.raises(ValueError, match=f"Meal with ID {meal.id} has been deleted"):
        delete_meal(meal.id)

##################################################
# Meal Retrieval Test Cases
##################################################

def test_get_meal_by_id(meal_instance):
    """Test retrieving a meal by ID."""
    create_meal(meal_instance.meal, meal_instance.cuisine, meal_instance.price, meal_instance.difficulty)
    meal = get_meal_by_id(meal_instance.id)

    assert meal.id == meal_instance.id
    assert meal.meal == meal_instance.meal
    assert meal.cuisine == meal_instance.cuisine
    assert meal.price == meal_instance.price
    assert meal.difficulty == meal_instance.difficulty

def test_get_meal_by_name(meal_instance):
    """Test retrieving a meal by name."""
    create_meal(meal_instance.meal, meal_instance.cuisine, meal_instance.price, meal_instance.difficulty)
    meal = get_meal_by_name(meal_instance.meal)

    assert meal.id == meal_instance.id
    assert meal.meal == meal_instance.meal
    assert meal.cuisine == meal_instance.cuisine
    assert meal.price == meal_instance.price
    assert meal.difficulty == meal_instance.difficulty

def test_get_non_existent_meal_by_id():
    """Test retrieving a meal by ID that does not exist."""
    with pytest.raises(ValueError, match="Meal with ID 999 not found"):
        get_meal_by_id(999)

def test_get_non_existent_meal_by_name():
    """Test retrieving a meal by name that does not exist."""
    with pytest.raises(ValueError, match="Meal with name 'Non-existent Meal' not found"):
        get_meal_by_name('Non-existent Meal')

##################################################
# Meal Stats Update Test Cases
##################################################

def test_update_meal_stats(meal_instance):
    """Test updating the stats of a meal after a battle."""
    create_meal(meal_instance.meal, meal_instance.cuisine, meal_instance.price, meal_instance.difficulty)
    update_meal_stats(meal_instance.id, 'win')

    meal = get_meal_by_id(meal_instance.id)
    assert meal.battles == 1
    assert meal.wins == 1

    update_meal_stats(meal_instance.id, 'loss')
    meal = get_meal_by_id(meal_instance.id)
    assert meal.battles == 2
    assert meal.wins == 1

def test_update_non_existent_meal_stats():
    """Test error when updating stats for a non-existent meal."""
    with pytest.raises(ValueError, match="Meal with ID 999 not found"):
        update_meal_stats(999, 'win')

def test_update_deleted_meal_stats(meal_instance):
    """Test error when updating stats for a deleted meal."""
    create_meal(meal_instance.meal, meal_instance.cuisine, meal_instance.price, meal_instance.difficulty)
    meal = get_meal_by_name(meal_instance.meal)
    delete_meal(meal.id)

    with pytest.raises(ValueError, match=f"Meal with ID {meal.id} has been deleted"):
        update_meal_stats(meal.id, 'win')
