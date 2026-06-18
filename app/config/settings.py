from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置，统一读取环境变量和 .env 文件。"""

    app_name: str = "跨境电商物流 AI 优化助手"
    environment: str = "local"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/logistics_ai"
    redis_url: str = "redis://localhost:6379/0"
    default_currency: str = "USD"
    carrier_mode: Literal["mock", "real", "mixed"] = "mock"
    carrier_timeout_seconds: float = 8.0
    carrier_retry_count: int = 2
    task_status_persistence_enabled: bool = False
    shippo_api_key: str = ""
    dhl_api_key: str = ""
    fedex_api_key: str = ""
    ups_api_key: str = ""
    aftership_api_key: str = ""
    model_service_url: str = ""
    llm_service_url: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """获取应用配置单例。"""
    return Settings()
