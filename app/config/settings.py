from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置，统一读取环境变量和 .env 文件。"""

    app_name: str = "跨境电商物流 AI 优化助手"
    environment: str = "local"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/logistics_ai"
    redis_url: str = "redis://localhost:6379/0"
    default_currency: str = "USD"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """获取应用配置单例。"""
    return Settings()
