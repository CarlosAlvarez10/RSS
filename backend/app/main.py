from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import alerts, cai, customers, email_logs, fiscal_data, health, invoices, payments, reports, storeganise, webhooks_bac, webhooks_storeganise
from app.core.config import get_settings
from app.core.exceptions import BusinessRuleError, DuplicateEventError, ExternalProviderError


settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(BusinessRuleError)
async def business_rule_handler(_: Request, exc: BusinessRuleError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(DuplicateEventError)
async def duplicate_handler(_: Request, exc: DuplicateEventError):
    return JSONResponse(status_code=200, content={"detail": str(exc), "status": "DUPLICATE_BLOCKED"})


@app.exception_handler(ExternalProviderError)
async def provider_handler(_: Request, exc: ExternalProviderError):
    return JSONResponse(status_code=502, content={"detail": str(exc)})


app.include_router(health.router)
app.include_router(webhooks_storeganise.router)
app.include_router(webhooks_bac.router)
app.include_router(payments.router)
app.include_router(invoices.router)
app.include_router(customers.router)
app.include_router(fiscal_data.router)
app.include_router(cai.router)
app.include_router(reports.router)
app.include_router(alerts.router)
app.include_router(email_logs.router)
app.include_router(storeganise.router)
