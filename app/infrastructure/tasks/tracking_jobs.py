from app.infrastructure.tasks.celery_app import celery_app
from app.infrastructure.tasks.status import record_task_status


@celery_app.task(name="tracking.sync_status")  # type: ignore[untyped-decorator]
def sync_tracking_status() -> dict[str, str]:
    """同步物流轨迹任务，供 Celery Beat 定时调用。"""
    return record_task_status("tracking.sync_status", "scheduled")
