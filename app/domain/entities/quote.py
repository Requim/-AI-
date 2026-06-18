from dataclasses import dataclass
from datetime import UTC, datetime

from app.domain.entities.order import Order


@dataclass(frozen=True)
class QuoteRequest:
    """物流报价请求，保存订单和请求时间。"""

    order: Order
    requested_at: datetime = datetime.now(UTC)
