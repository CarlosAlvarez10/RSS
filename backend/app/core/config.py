from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Roatan Self Storage Integrator"
    api_prefix: str = ""
    environment: str = "development"
    database_url: str = "postgresql+psycopg://user:password@localhost:5432/roatanselfstorage"
    dashboard_origin: str = "http://localhost:3000"
    storeganise_webhook_secret: str = "change-me-storeganise-secret"
    bac_webhook_secret: str = "change-me-bac-secret"
    storeganise_api_base_url: str = "https://api.storeganise.com"
    storeganise_api_token: str = ""
    bac_simulator_base_url: str = "https://bac-simulator.local/pay"
    company_email_from: str = "facturacion@roatanselfstorage.com"
    alert_recipients: str = "admin@roatanselfstorage.com,contador@roatanselfstorage.com"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.dashboard_origin.split(",") if origin.strip()]

    @property
    def alert_email_list(self) -> list[str]:
        return [email.strip() for email in self.alert_recipients.split(",") if email.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
