import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import field_validator, Field

from app.utils.logging import setup_logging

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

class Settings(BaseSettings):
    # Общие настройки
    LOG_DIR: Path = Field(default=BASE_DIR / "app/logs")
    LOG_LEVEL: str = "INFO"

    # Общий User-Agent для всех HTTP-запросов
    # DEFAULT_USER_AGENT: str = "osm-service/1.0 (your_email@example.com)"
    DEFAULT_USER_AGENT: str = "osm-service/1.0 (anton42@yandex.ru)"

    # Nominatim API
    NOMINATIM_URL: str = "https://nominatim.openstreetmap.org/"
    NOMINATIM_USER_AGENT: str | None = None

    # Overpass API
    OVERPASS_URL: str = "https://overpass-api.de/api/interpreter"
    OVERPASS_USER_AGENT: str | None = None

    # OSRM (может быть локальным)
    OSRM_URL: str = "http://router.project-osrm.org"
    OSRM_USER_AGENT: str | None = None
    
    # # Координаты Белгородской области (по умолчанию)
    # DEFAULT_BBOX: tuple[float, float, float, float] = (36.0, 51.5, 38.5, 51.0)  # left, top, right, bottom
    # DEFAULT_CENTER: tuple[float, float] = (51.25, 37.25)  # lat, lon
    
    # Координаты по умолчанию (Белгород)
    DEFAULT_CENTER: tuple[float, float] = (50.5954, 36.5872)  # lat, lon
    DEFAULT_BBOX: tuple[float, float, float, float] = (36.55, 50.62, 36.63, 50.57)  # left, top, right, bottom

    @field_validator("LOG_DIR", mode="before")
    @classmethod
    def validate_paths(cls, value: str) -> Path:
        path = Path(value)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_user_agent(self, service: str) -> str:
        """Возвращает User-Agent для указанного сервиса, либо значение по умолчанию."""
        return getattr(self, f"{service.upper()}_USER_AGENT") or self.DEFAULT_USER_AGENT

settings = Settings()

setup_logging(log_dir=settings.LOG_DIR, log_level=settings.LOG_LEVEL)
