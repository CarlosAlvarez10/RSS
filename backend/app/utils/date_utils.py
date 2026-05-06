from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


def iso_now() -> str:
    return utc_now().isoformat()


def days_until(value: datetime) -> int:
    return (value.date() - utc_now().date()).days
