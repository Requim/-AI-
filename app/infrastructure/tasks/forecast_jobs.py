from app.infrastructure.tasks.celery_app import celery_app


@celery_app.task(name="inventory.refresh_forecasts")  # type: ignore[untyped-decorator]
def refresh_inventory_forecasts() -> dict[str, str]:
    """刷新库存预测任务，供 Celery Beat 定时调用。"""
    return {"status": "scheduled"}
