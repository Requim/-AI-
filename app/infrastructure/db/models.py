from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """SQLAlchemy 模型基类。"""


class ShipmentModel(Base):
    """物流方案表，用于持久化推荐结果。"""

    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[str] = mapped_column(String(64), index=True)
    carrier: Mapped[str] = mapped_column(String(64))
    service: Mapped[str] = mapped_column(String(64))
    cost: Mapped[float] = mapped_column(Numeric(12, 2))
    estimated_days: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[str] = mapped_column(DateTime)
