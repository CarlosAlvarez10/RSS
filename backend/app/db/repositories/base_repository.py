from dataclasses import asdict, is_dataclass
from typing import Any
from app.db.session import InMemoryDatabase, get_db


class BaseRepository:
    table_name = "base"

    def __init__(self, database: InMemoryDatabase | None = None) -> None:
        self.db = database or get_db()

    def add(self, item: Any) -> Any:
        key = getattr(item, "id", None) or getattr(item, "payment_id", None)
        with self.db.lock:
            self.db.tables[self.table_name][key] = item
        return item

    def get(self, item_id: str) -> Any | None:
        return self.db.tables[self.table_name].get(item_id)

    def list(self) -> list[Any]:
        return list(self.db.tables[self.table_name].values())

    def update(self, item_id: str, **values: Any) -> Any | None:
        with self.db.lock:
            item = self.get(item_id)
            if not item:
                return None
            for key, value in values.items():
                setattr(item, key, value)
            return item

    def find_by(self, **criteria: Any) -> list[Any]:
        return [item for item in self.list() if all(getattr(item, key, None) == value for key, value in criteria.items())]

    def to_dict(self, item: Any) -> dict[str, Any]:
        return asdict(item) if is_dataclass(item) else dict(item)
