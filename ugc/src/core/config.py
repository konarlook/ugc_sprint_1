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


class AuthJWTSettings(_BaseSettings):
    """JWT settings for check privileges"""

    public_key: Path = Path(__file__).parent / "certs" / "public.pem"
    auth_algorithm_password: str = Field(
        default="RS256",
        description="Token encryption algorithm",
    )
    access_token_lifetime: int = Field(
        default=3600,
        description="Lifetime of access tokens in seconds",
    )
    refresh_token_lifetime: int = Field(
        default=86400,
        description="Refresh token lifetime in seconds",
    )


class KafkaSettings(_BaseSettings):
    """Kafka settings for service"""

    kafka_dsn: KafkaDsn | None = Field(default=None)
    kafka_topic: str | None = Field(default=None)


class Settings(CommonSettings):
    """Main class for combine settings"""

    auth_jwt: AuthJWTSettings = AuthJWTSettings()
    kafka: KafkaSettings = KafkaSettings()


settings = Settings()
