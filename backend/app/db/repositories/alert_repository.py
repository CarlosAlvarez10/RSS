from app.db.repositories.base_repository import BaseRepository


class AlertRepository(BaseRepository):
    table_name = "alerts"
