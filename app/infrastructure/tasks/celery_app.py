from celery import Celery

from app.config.settings import get_settings


def create_celery_app() -> Celery:
    """创建 Celery 应用，用于轨迹同步和库存预测任务。"""
    settings = get_settings()
    celery = Celery("logistics_ai", broker=settings.redis_url, backend=settings.redis_url)
    celery.conf.timezone = "Asia/Shanghai"
    celery.autodiscover_tasks(["app.infrastructure.tasks"])
    return celery


celery_app = create_celery_app()
