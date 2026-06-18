from typing import Protocol

from app.domain.entities.order import Order
from app.domain.entities.route_option import RouteOption


class RouteOptimizer(Protocol):
    """物流路线优化接口，用于对候选方案进行排序。"""

    def rank(self, order: Order, options: list[RouteOption]) -> list[RouteOption]:
        """根据成本、时效、风险和预算对物流方案排序。"""
        ...
