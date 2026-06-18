from typing import Protocol

from app.domain.entities.inventory import InventoryForecast
from app.domain.entities.ml import MarketContext
from app.domain.entities.route_option import RouteOption
from app.domain.value_objects.risk_score import RiskScore


class MLPredictor(Protocol):
    """机器学习预测接口，用于预测延误、成本和库存需求。"""

    def predict_delay_risk(self, option: RouteOption, context: MarketContext) -> RiskScore:
        """预测物流方案的延误风险。"""
        ...

    def predict_demand(self, sku: str, days: int, context: MarketContext) -> InventoryForecast:
        """预测指定 SKU 在未来若干天的需求量。"""
        ...
