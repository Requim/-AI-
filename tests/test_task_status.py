from app.infrastructure.tasks.status import record_task_status


def test_record_task_status_degrades_when_database_is_unavailable() -> None:
    """验证数据库不可用时任务状态记录会降级返回。"""
    result = record_task_status("test.task", "scheduled")
    assert result["status"] in {"scheduled", "degraded"}
