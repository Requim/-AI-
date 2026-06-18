import asyncio
from collections.abc import Sequence

from app.domain.entities.ml import MarketContext
from app.domain.entities.order import Order
from app.domain.entities.quote import QuoteRequest
from app.domain.entities.recommendation import RecommendationResult
from app.domain.entities.route_option import RouteOption
from app.domain.ports.carrier_gateway import CarrierGateway
from app.domain.ports.ml_predictor import MLPredictor
from app.domain.ports.route_optimizer import RouteOptimizer


class RecommendShippingUseCase:
    """物流推荐用例，负责报价采集、风险预测和路线排序。"""

    def __init__(
        self,
        carriers: Sequence[CarrierGateway],
        optimizer: RouteOptimizer,
        predictor: MLPredictor,
    ) -> None:
        """初始化物流推荐用例。"""
        self._carriers = list(carriers)
        self._optimizer = optimizer
        self._predictor = predictor

    async def execute(self, order: Order) -> RecommendationResult:
        """执行物流推荐并返回按优先级排序的方案。"""
        request = QuoteRequest(order)
        options = await self._collect_quotes(request)
        context = MarketContext(region=order.destination.region)
        enriched = self._apply_predictions(options, context)
        ranked = self._optimizer.rank(order, enriched)
        return RecommendationResult(ranked)

    async def _collect_quotes(self, request: QuoteRequest) -> list[RouteOption]:
        tasks = [carrier.get_quote(request) for carrier in self._carriers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        valid_groups = [item for item in results if isinstance(item, list)]
        return [option for group in valid_groups for option in group]

    def _apply_predictions(
        self,
        options: list[RouteOption],
        context: MarketContext,
    ) -> list[RouteOption]:
        return [
            option.with_risk(self._predictor.predict_delay_risk(option, context))
            for option in options
        ]
