from app.db.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    table_name = "customers"

    def get_by_storeganise_user_id(self, user_id: str):
        matches = self.find_by(storeganise_user_id=user_id)
        return matches[0] if matches else None
