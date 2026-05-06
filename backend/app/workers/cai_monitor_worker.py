from app.services.cai_service import CaiService


def monitor_cai_ranges() -> dict:
    return {"status": "COMPLETED", "alerts": CaiService().monitor()}
