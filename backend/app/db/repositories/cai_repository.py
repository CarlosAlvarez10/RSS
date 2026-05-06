from app.core.constants import CaiStatus
from app.db.repositories.base_repository import BaseRepository


class CaiRepository(BaseRepository):
    table_name = "cai_ranges"

    def get_active(self, document_type: str = "01", branch: str = "001", emission_point: str = "002"):
        matches = [
            item for item in self.list()
            if item.status == CaiStatus.ACTIVE and item.document_type == document_type and item.branch == branch and item.emission_point == emission_point
        ]
        return matches[0] if matches else None
