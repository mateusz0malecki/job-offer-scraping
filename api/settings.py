from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_user: str
    postgres_db: str
    postgres_password: str
    postgres_host: str
    celery_broker_url: str
    celery_result_backend: str
    amqp_host: str
    amqp_uri: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
