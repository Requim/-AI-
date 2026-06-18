from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import JSON, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """SQLAlchemy 模型基类。"""


class OrderModel(Base):
    """订单表，用于持久化物流推荐输入。"""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    sku: Mapped[str] = mapped_column(String(128), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    destination: Mapped[dict[str, str]] = mapped_column(JSON)
    package: Mapped[dict[str, str]] = mapped_column(JSON)
    requirement: Mapped[dict[str, str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))


class ShipmentModel(Base):
    """物流方案表，用于持久化推荐结果。"""

    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[str] = mapped_column(String(64), index=True)
    carrier: Mapped[str] = mapped_column(String(64))
    service: Mapped[str] = mapped_column(String(64))
    cost: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    estimated_days: Mapped[int] = mapped_column(Integer)
    risk_score: Mapped[int] = mapped_column(Integer)
    reasons: Mapped[list[str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))


class TrackingEventModel(Base):
    """轨迹事件表，用于保存最新状态和异常预警。"""

    __tablename__ = "tracking_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tracking_no: Mapped[str] = mapped_column(String(128), index=True)
    carrier: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(64))
    latest_location: Mapped[str] = mapped_column(String(255))
    alerts: Mapped[list[str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))


class InventoryForecastModel(Base):
    """库存预测表，用于保存预测销量和补货建议。"""

    __tablename__ = "inventory_forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(128), index=True)
    region: Mapped[str] = mapped_column(String(64), index=True)
    forecast_days: Mapped[int] = mapped_column(Integer)
    predicted_units: Mapped[int] = mapped_column(Integer)
    reorder_units: Mapped[int] = mapped_column(Integer)
    reasons: Mapped[list[str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))


class ProfitResultModel(Base):
    """利润结果表，用于保存成本利润分析结果。"""

    __tablename__ = "profit_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(128), index=True)
    gross_profit: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    net_profit: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    profit_margin: Mapped[Decimal] = mapped_column(Numeric(8, 4))
    risk_items: Mapped[list[str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))


class TaskStatusModel(Base):
    """后台任务状态表，用于记录任务执行结果和错误信息。"""

    __tablename__ = "task_statuses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_name: Mapped[str] = mapped_column(String(128), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
