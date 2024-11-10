from typing import Any

from wildlife_tracker.migration_tracking.migration_path import MigrationPath

class Migration:

    def __init__(self, migration_id: int, migration_path: MigrationPath, duration: Optional[int] = None) -> None:
        self.migration_id = migration_id
        self.migration_path = migration_path
        self.duration = duration

    def get_migration_details(migration_id: int) -> dict[str, Any]:
        pass

    def update_migration_details(migration_id: int, **kwargs: Any) -> None:
        pass