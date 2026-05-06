from app.services.email_service import EmailService


def retry_failed_emails() -> dict:
    retried = EmailService().retry_failed()
    return {"status": "COMPLETED", "retried": len(retried)}
