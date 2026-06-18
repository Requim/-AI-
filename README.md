# 跨境电商物流 AI 优化助手

这是一个 Python 模块化单体后端，按 Clean Architecture 组织代码，通过抽象端口隔离承运商 API、数据库、优化器、机器学习模型和 LLM。

当前版本已经支持 **Mock / Real / Mixed** 三种外部模块接入模式。默认本地使用 Mock，后续可以通过环境变量逐步切换到真实承运商、真实数据库、模型服务和 RAG/LLM。

## 当前能力

- 物流推荐：`POST /quotes/recommend`
- 物流轨迹：`GET /tracking/{tracking_no}`
- 库存预测：`POST /inventory/forecast`
- 利润计算：`POST /profit/calculate`
- AI 助手：`POST /assistant/ask`

## 架构分层

```text
app/
  api/              HTTP 入参校验、响应转换、路由
  application/      用例编排，不依赖外部 SDK
  domain/           实体、值对象、业务规则、端口契约
  infrastructure/   承运商、HTTP、数据库、Celery、ML、LLM 适配器
  config/           环境配置
alembic/            数据库迁移
tests/              单元测试、接口测试、契约测试
```

核心原则：`api`、`application`、`domain` 不直接依赖第三方 API。真实外部模块只在 `infrastructure` 下新增 Adapter。

## 快速运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

OpenAPI 文档：

- <http://127.0.0.1:8000/docs>

## 外部模块接入模式

`.env` 中通过 `CARRIER_MODE` 控制承运商来源：

```env
CARRIER_MODE=mock
```

- `mock`：只使用 `MockCarrierGateway`，适合本地开发和测试。
- `real`：只使用真实承运商 Adapter，需要配置 API Key。
- `mixed`：同时使用 Mock 和真实 Adapter，适合灰度联调。

真实承运商配置示例：

```env
CARRIER_MODE=real
SHIPPO_API_KEY=xxx
DHL_API_KEY=xxx
FEDEX_API_KEY=xxx
UPS_API_KEY=xxx
AFTERSHIP_API_KEY=xxx
CARRIER_TIMEOUT_SECONDS=8
CARRIER_RETRY_COUNT=2
```

不要把真实 API Key 提交到仓库。

## 新增真实承运商

1. 实现 `domain.ports.CarrierGateway`。
2. 在 Adapter 内完成外部请求、响应转换、错误映射。
3. 在 `infrastructure/carriers/external_carriers.py` 注册配置。
4. 增加 contract test，验证输出仍是 `RouteOption` 和 `TrackingStatus`。

主流程不需要修改：

```text
RecommendShippingUseCase -> CarrierGateway -> RealCarrierGateway
UpdateTrackingStatusUseCase -> CarrierGateway -> RealCarrierGateway
```

## 数据库与迁移

当前已提供 Alembic 骨架和一期表结构：

- `orders`
- `shipments`
- `tracking_events`
- `inventory_forecasts`
- `profit_results`
- `task_statuses`

执行迁移：

```powershell
alembic upgrade head
```

数据库连接来自：

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/logistics_ai
```

## 异步任务

Celery 使用 Redis：

```env
REDIS_URL=redis://localhost:6379/0
```

任务入口：

- `tracking.sync_status`
- `inventory.refresh_forecasts`

默认本地不写入 `task_statuses`，避免没有 PostgreSQL 时任务阻塞。需要记录任务状态时启用：

```env
TASK_STATUS_PERSISTENCE_ENABLED=true
```

启用后数据库不可用会返回 `degraded`，不阻断任务进程。

## 质量门禁

```powershell
python scripts/check_code_constraints.py app tests scripts
python -m pytest
python -m ruff check app tests scripts
python -m mypy app tests scripts
```

编码约束：

- 对外暴露 API、端口、公共方法使用中文注释。
- 单个函数或方法非空非注释代码行不超过 50。
- 代码嵌套层级不超过 3。

## 渐进式推进路线

1. 配置化替换 Mock：已完成。
2. 接入第一个真实承运商：优先 Shippo 或 4PX，补齐真实字段映射。
3. 落库与任务化：补 Repository 调用点，保存推荐、轨迹、利润和库存结果。
4. 多承运商与预警：接入 DHL/FedEx/UPS/AfterShip，增加限流、错误码和降级。
5. 预测和 AI 助手增强：接入模型服务、向量库和 LLM 工具调用。
