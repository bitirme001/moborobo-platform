from functools import lru_cache
from os import getenv

from dotenv import load_dotenv


load_dotenv()


class Settings:
    database_url: str
    frontend_origins: list[str]

    def __init__(self) -> None:
        self.database_url = getenv("DATABASE_URL", "sqlite:///./moborobo.db")
        origins = getenv(
            "FRONTEND_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        )
        self.frontend_origins = [origin.strip() for origin in origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
