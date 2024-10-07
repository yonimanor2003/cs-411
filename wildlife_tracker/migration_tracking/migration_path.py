from typing import Optional

from wildlife_tracker.habitat_management.habitat import Habitat

class MigrationPath:

    def __init__(self, path_id: int, start_date: str, start_location: Habitat, destination: Habitat) -> None:
        self.path_id = path_id
        self.start_date = start_date
        self.start_location = start_location
        self.destination = destination

    def get_habitat_by_id(habitat_id: int) -> Habitat:
        pass

    def get_migration_path_details(path_id) -> dict:
        pass

    def update_migration_path_details(path_id: int, **kwargs) -> None:
        pass