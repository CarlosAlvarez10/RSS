from collections import defaultdict
from threading import RLock
from typing import Any


class InMemoryDatabase:
    """Development storage with the same repository shape expected for Neon/PostgreSQL."""

    def __init__(self) -> None:
        self.lock = RLock()
        self.tables: dict[str, dict[str, Any]] = defaultdict(dict)


db = InMemoryDatabase()


def get_db() -> InMemoryDatabase:
    return db
