from fastapi import APIRouter
from app.schemas.cai_schema import CaiCreate
from app.services.cai_service import CaiService


router = APIRouter(prefix="/cai", tags=["cai-correlatives"])


@router.post("")
def register_cai(payload: CaiCreate):
    return CaiService().register(payload)


@router.get("")
def list_cai():
    service = CaiService()
    return [{"range": item, "available": service.available(item), "used": service.used(item)} for item in service.cai_ranges.list()]


@router.post("/{cai_id}/activate")
def activate_cai(cai_id: str):
    return CaiService().activate(cai_id)


@router.post("/{cai_id}/deactivate")
def deactivate_cai(cai_id: str):
    return CaiService().deactivate(cai_id)


@router.post("/monitor")
def monitor_cai():
    return {"alerts": CaiService().monitor()}
