from pathlib import Path
from pydantic import Field, KafkaDsn
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parents[4]


class _BaseSettings(BaseSettings):
    """Changing the base class settings"""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class CommonSettings(_BaseSettings):
    """Base settings for service"""

    service_name: str = Field(default="ugc", description="Name of service")


class KafkaSettings(_BaseSettings):
    """Kafka settings for service"""

    kafka_dsn: KafkaDsn
    kafka_topic: str


class Settings(CommonSettings):
    """Main class for combine settings"""

    kafka = KafkaSettings()


settings = Settings()
