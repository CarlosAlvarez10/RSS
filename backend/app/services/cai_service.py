from datetime import date
from threading import RLock
from app.core.constants import AlertLevel, CaiStatus
from app.core.exceptions import BusinessRuleError
from app.db.repositories.cai_repository import CaiRepository
from app.models.cai_range import CaiRange
from app.services.alert_service import AlertService
from app.utils.date_utils import utc_now
from app.utils.id_generator import new_id


class CaiService:
    """Fiscal CAI/correlative control. Replace lock with DB row lock in production."""

    def __init__(self, cai_ranges: CaiRepository | None = None, alerts: AlertService | None = None) -> None:
        self.cai_ranges = cai_ranges or CaiRepository()
        self.alerts = alerts or AlertService()
        self._lock = RLock()

    def register(self, payload) -> CaiRange:
        if payload.status == CaiStatus.ACTIVE and self.cai_ranges.get_active(payload.document_type, payload.branch, payload.emission_point):
            raise BusinessRuleError("Solo puede existir un CAI activo por tipo de documento, sucursal y punto de emisión.")
        cai = CaiRange(id=new_id("cai"), **payload.model_dump())
        return self.cai_ranges.add(cai)

    def activate(self, cai_id: str) -> CaiRange:
        target = self.cai_ranges.get(cai_id)
        if not target:
            raise BusinessRuleError("CAI no encontrado.")
        for item in self.cai_ranges.list():
            if item.document_type == target.document_type and item.branch == target.branch and item.emission_point == target.emission_point:
                item.status = CaiStatus.INACTIVE
        target.status = CaiStatus.ACTIVE
        return target

    def deactivate(self, cai_id: str) -> CaiRange | None:
        return self.cai_ranges.update(cai_id, status=CaiStatus.INACTIVE)

    def available(self, cai: CaiRange) -> int:
        return max(cai.range_end - cai.current_number, 0)

    def used(self, cai: CaiRange) -> int:
        return max(cai.current_number - cai.range_start + 1, 0)

    def validate_active(self) -> CaiRange:
        active = self.cai_ranges.get_active()
        if not active:
            self.alerts.create(AlertLevel.CRITICAL, "No hay CAI activo", "No se puede emitir factura fiscal.", "CAI")
            raise BusinessRuleError("No hay CAI activo.")
        if active.status != CaiStatus.ACTIVE:
            raise BusinessRuleError("El CAI no está activo.")
        if active.expiration_date < utc_now().date():
            self.alerts.create(AlertLevel.CRITICAL, "CAI vencido", "El CAI activo está vencido.", "CAI", active.id)
            raise BusinessRuleError("El CAI está vencido.")
        if self.available(active) <= 0:
            self.alerts.create(AlertLevel.CRITICAL, "Correlativos agotados", "No hay correlativos disponibles.", "CAI", active.id)
            raise BusinessRuleError("El rango está agotado.")
        return active

    def consume_next_correlative(self) -> tuple[CaiRange, int]:
        with self._lock:
            active = self.validate_active()
            next_correlative = active.current_number + 1
            if next_correlative > active.range_end:
                active.status = CaiStatus.EXHAUSTED
                raise BusinessRuleError("El rango quedó agotado.")
            active.current_number = next_correlative
            remaining = self.available(active)
            if remaining in {100, 50, 25}:
                self.alerts.create(AlertLevel.WARNING if remaining > 25 else AlertLevel.CRITICAL, "Correlativos bajos", f"Quedan {remaining} correlativos.", "CAI", active.id)
            return active, next_correlative

    def monitor(self) -> list[str]:
        created: list[str] = []
        for item in self.cai_ranges.list():
            days = (item.expiration_date - date.today()).days
            if item.status == CaiStatus.ACTIVE and days in {30, 15, 7}:
                created.append(self.alerts.cai_expiring(item.id, days).id)
            if self.available(item) in {100, 50, 25, 0}:
                created.append(self.alerts.create(AlertLevel.WARNING, "Correlativos bajos", f"Quedan {self.available(item)} correlativos.", "CAI", item.id).id)
        return created
