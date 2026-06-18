from fastapi import FastAPI

from app.api.routes import (
    assistant_routes,
    inventory_routes,
    profit_routes,
    quote_routes,
    tracking_routes,
)
from app.config.settings import get_settings


def create_app() -> FastAPI:
    """创建 FastAPI 应用并注册所有业务路由。"""
    settings = get_settings()
    api = FastAPI(title=settings.app_name, version="0.1.0")
    api.include_router(quote_routes.router)
    api.include_router(tracking_routes.router)
    api.include_router(inventory_routes.router)
    api.include_router(profit_routes.router)
    api.include_router(assistant_routes.router)
    return api


app = create_app()
