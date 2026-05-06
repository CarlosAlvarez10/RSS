import hashlib
import hmac
from fastapi import Header, HTTPException, Request, status
from app.core.config import get_settings


def hmac_sha256(raw_body: bytes, secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()


def constant_time_compare(left: str, right: str) -> bool:
    return hmac.compare_digest(left.strip(), right.strip())


async def verify_storeganise_signature(request: Request, sg_signature: str | None = Header(default=None)) -> bytes:
    raw_body = await request.body()
    expected = hmac_sha256(raw_body, get_settings().storeganise_webhook_secret)
    if not sg_signature or not constant_time_compare(sg_signature, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Storeganise signature")
    return raw_body


async def verify_bac_signature(request: Request, x_bac_signature: str | None = Header(default=None)) -> bytes:
    raw_body = await request.body()
    expected = hmac_sha256(raw_body, get_settings().bac_webhook_secret)
    if get_settings().environment != "development" and (not x_bac_signature or not constant_time_compare(x_bac_signature, expected)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid BAC signature")
    return raw_body
