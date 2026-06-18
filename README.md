# 跨境电商物流 AI 优化助手

这是一个 Python 模块化单体后端骨架，按 Clean Architecture 组织代码，并通过抽象端口隔离数据库、承运商 API、优化器、机器学习模型和 LLM。

## 技术栈

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL / TimescaleDB
- Redis / Celery
- OR-Tools
- Pydantic
- pytest / ruff / mypy

默认实现使用 Mock 承运商、规则型预测器、启发式路线优化器和本地 AI 助手，便于先跑通业务链路。

## 快速运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## 接口

- `POST /quotes/recommend`：推荐物流方案。
- `GET /tracking/{tracking_no}`：查询物流轨迹并检测异常。
- `POST /inventory/forecast`：预测库存和补货建议。
- `POST /profit/calculate`：计算成本和利润。
- `POST /assistant/ask`：生成式 AI 助手问答。

## 代码约束

```powershell
python scripts/check_code_constraints.py app tests scripts
```

检查内容：

- 单个函数或方法非空非注释行不超过 50。
- 代码嵌套层级不超过 3。

## 设计原则

- API 层只做 HTTP 协议转换。
- Application 层编排用例。
- Domain 层保存核心实体、规则和端口。
- Infrastructure 层实现数据库、承运商、ML、LLM、任务队列等外部能力。
- 新增承运商只需实现对应端口，不修改推荐主流程。
