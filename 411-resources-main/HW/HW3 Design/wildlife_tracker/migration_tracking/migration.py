from typing import Any, Optional

from wildlife_tracker.migration_management.migration_path import MigrationPath


class Migration:
    def __init__( self, migration_id: int, migration_path: MigrationPath, status: str = "Scheduled", current_location: Optional[str] = None, current_date: Optional[str] = None) -> None:
        self.migration_id = migration_id
        self.migration_path = migration_path
        self.status = status
        self.current_location = current_location
        self.current_date = current_date

    def update_migration_details(self, **kwargs: Any) -> None:
        pass

    def get_migration_details(self) -> dict[str, Any]:
        pass
