from typing import Protocol

from app.domain.entities.inventory import InventoryForecast
from app.domain.entities.order import Order
from app.domain.entities.profit import ProfitResult
from app.domain.entities.recommendation import RecommendationResult
from app.domain.entities.tracking import TrackingResult


class OrderRepository(Protocol):
    """订单仓储接口，用于保存和查询订单。"""

    def save(self, order: Order) -> None:
        """保存订单核心信息。"""
        ...


class RecommendationRepository(Protocol):
    """物流推荐仓储接口，用于保存推荐结果。"""

    def save(self, order_id: str, result: RecommendationResult) -> None:
        """保存订单对应的物流推荐结果。"""
        ...


class TrackingRepository(Protocol):
    """物流轨迹仓储接口，用于保存轨迹状态和异常预警。"""

    def save(self, result: TrackingResult) -> None:
        """保存物流轨迹状态和异常预警。"""
        ...


class InventoryForecastRepository(Protocol):
    """库存预测仓储接口，用于保存预测结果。"""

    def save(self, forecast: InventoryForecast) -> None:
        """保存库存预测结果。"""
        ...


class ProfitResultRepository(Protocol):
    """利润结果仓储接口，用于保存利润计算结果。"""

    def save(self, result: ProfitResult) -> None:
        """保存利润计算结果。"""
        ...
