from fastapi import APIRouter
from app.core.config import get_settings


router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {"status": "ok", "app": get_settings().app_name, "database": "configured", "storeganise": "configured", "bac": "simulator"}
