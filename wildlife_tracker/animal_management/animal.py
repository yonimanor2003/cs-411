from typing import Any, Optional

from wildlife_tracker.animal_managment.animal import Animal

class Animal:

    def __init__(self, animal_id: int, species: str, current_date: str, current_location: str, health_status: Optional[str] = None, age: Optional[int] = None) -> None:
        self.animal_id = animal_id
        self.species = species
        self.current_location = current_location
        self.current_date = current_date
        self.health_status = health_status
        self.age = age

    def get_animal_details(animal_id) -> dict[str, Any]:
        pass

    def update_animal_details(animal_id: int, **kwargs: Any) -> None:
        pass

    def assign_animals_to_habitat(habitat_id: int, animals: List[Animal]) -> None:
        pass

    
    


