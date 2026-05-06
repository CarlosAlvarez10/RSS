from app.db.repositories.base_repository import BaseRepository
from app.models.audit_log import AuditLog
from app.utils.id_generator import new_id


class AuditRepository(BaseRepository):
    table_name = "audit_logs"


class AuditService:
    def __init__(self, audits: AuditRepository | None = None) -> None:
        self.audits = audits or AuditRepository()

    def record(self, action: str, module: str, entity_id: str, old_value: dict | None = None, new_value: dict | None = None, user_id: str = "system") -> AuditLog:
        return self.audits.add(AuditLog(id=new_id("audit"), action=action, module=module, entity_id=entity_id, old_value=old_value, new_value=new_value, user_id=user_id))
