import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8081
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/microservices_demo")
    debug: bool = False

def get_settings() -> Settings:
    return Settings()