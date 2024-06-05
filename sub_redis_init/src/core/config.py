import os

from dotenv import find_dotenv, load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class _BaseSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class CommonSettings(_BaseSettings):
    service_name: str = Field(
        default="auth",
        description="Init Redis для хранения данных о подписках пользователей",
    )
    base_dir: str = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        description="Корень проекта",
    )
    debug_mode: bool = Field(
        default=False,
        description="Режим отладки сервиса авторизации",
    )


class RedisSettings(_BaseSettings):
    host: str = Field(
        default="redis_subscription",
        description="Адрес хоста Redis для хранения данных о подписках",
    )
    port: int = Field(
        default=6379,
        description="Порт Redis для хранения данных о подписках",
    )
    password: str = Field(
        default="sub_pass",
        description="Пароль от Redis",
    )
    database: int = Field(
        default=0,
        description="База данных Redis для хранения данных о подписках",
    )

    @property
    def conn_data(self):
        conn_data = {
            'username': 'default',
            'password': self.password,
            'host': self.host,
            'port': self.port,
            'db': self.database,
        }

        return conn_data


class BillingApi(_BaseSettings):
    host: str = Field(
        default='billing_service',
        description="Хост сервиса оплаты",
        alias="BILLING_API_HOST"
    )
    port: int = Field(
        default=8000,
        description="Порт сервиса оплаты",
        alias="BILLING_API_PORT"
    )
    path: str = Field(
        default='backup_subscription',
        description="Путь к route",
        alias="BILLING_API_BACKUP_PATH"
    )

    @property
    def full_url(self):
        return f'{self.host}:{self.port}/{self.path}'


class Settings(CommonSettings):
    redis: RedisSettings = RedisSettings()

    billing: BillingApi = BillingApi()


settings = Settings()
