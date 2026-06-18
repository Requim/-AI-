from app.domain.entities.inventory import InventoryForecast, InventoryForecastRequest
from app.domain.entities.ml import MarketContext
from app.domain.ports.ml_predictor import MLPredictor


class PredictInventoryUseCase:
    """库存预测用例，负责把请求转换为预测上下文。"""

    def __init__(self, predictor: MLPredictor) -> None:
        """初始化库存预测用例。"""
        self._predictor = predictor

    def execute(self, request: InventoryForecastRequest) -> InventoryForecast:
        """执行库存需求预测。"""
        context = MarketContext(region=request.region, sales_history=request.sales_history)
        forecast = self._predictor.predict_demand(request.sku, request.days, context)
        return forecast.with_reorder_units(request.lead_time_days)
