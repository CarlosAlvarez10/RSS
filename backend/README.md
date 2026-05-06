# Roatan Self Storage Backend

Backend integrador FastAPI para Storeganise, BAC, CAI/correlativos, facturación fiscal, correos, alertas y reportes.

## Regla final del negocio

Storeganise genera la factura origen. El backend recibe el webhook, guarda el payload, espera datos fiscales, crea el pago BAC, valida la confirmación BAC, consume CAI/correlativo con bloqueo transaccional, genera factura fiscal, genera PDF, envía correo, actualiza Storeganise y expone el estado al dashboard.

## Eventos Storeganise

- unitRental.invoice.created
- invoice.updated
- invoice.state.updated
- invoice.payments.updated
- user.created
- user.updated
- user.billing.updated
- addon.dailyEvent.started

## Webhooks

- `POST /webhooks/storeganise`: requiere `sg-signature` HMAC SHA-256 sobre el body crudo.
- `POST /webhooks/bac`: listo para firma BAC real; en `development` permite simulación controlada.
- `POST /webhooks/bac/simulate`: simulador temporal de BAC.

## Desarrollo

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Neon PostgreSQL

La estructura ya separa modelos, repositorios y servicios. Los repositorios actuales son en memoria para desarrollo; el siguiente paso es cambiar `app/db/repositories` a SQLAlchemy contra Neon y agregar migraciones.
