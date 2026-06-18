from app.config.settings import get_settings
from app.infrastructure.db.repositories import SqlAlchemyTaskStatusRepository
from app.infrastructure.db.session import build_session_factory, session_scope


def record_task_status(task_name: str, status: str, message: str = "") -> dict[str, str]:
    """记录后台任务状态；数据库不可用时返回降级状态。"""
    if not get_settings().task_status_persistence_enabled:
        return {"status": status, "message": "persistence disabled"}
    try:
        _save_task_status(task_name, status, message)
    except Exception as exc:
        return {"status": "degraded", "message": str(exc)}
    return {"status": status, "message": message}


def _save_task_status(task_name: str, status: str, message: str) -> None:
    factory = build_session_factory()
    with session_scope(factory) as session:
        repository = SqlAlchemyTaskStatusRepository(session)
        repository.save(task_name, status, message)
