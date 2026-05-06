from pydantic import BaseModel


class StoreganiseWebhookPayload(BaseModel):
    id: str | None = None
    type: str
    data: dict = {}


class WebhookAccepted(BaseModel):
    ok: bool = True
    event_id: str
    status: str
