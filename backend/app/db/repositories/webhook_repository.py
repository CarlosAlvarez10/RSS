from app.db.repositories.base_repository import BaseRepository


class WebhookRepository(BaseRepository):
    table_name = "webhook_events"

    def get_by_event_id(self, provider: str, event_id: str):
        matches = self.find_by(provider=provider, event_id=event_id)
        return matches[0] if matches else None
