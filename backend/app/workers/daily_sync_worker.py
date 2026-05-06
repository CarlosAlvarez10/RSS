from app.services.cai_service import CaiService
from app.services.storeganise_service import StoreganiseService


def run_daily_sync() -> dict:
    StoreganiseService().handle_daily_event({"type": "addon.dailyEvent.started"})
    alerts = CaiService().monitor()
    return {"status": "COMPLETED", "cai_alerts": alerts}
