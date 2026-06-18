from decimal import Decimal

from pydantic import BaseModel

from app.domain.entities.assistant import AssistantAnswer
from app.domain.entities.inventory import InventoryForecast
from app.domain.entities.profit import ProfitResult
from app.domain.entities.recommendation import RecommendationResult
from app.domain.entities.route_option import RouteOption
from app.domain.entities.tracking import TrackingResult


class RouteOptionResponse(BaseModel):
    """物流方案响应模型，用于返回报价、时效、风险和推荐原因。"""

    carrier: str
    service: str
    cost: Decimal
    currency: str
    estimated_days: int
    risk_score: int
    risk_label: str
    score: Decimal
    reasons: list[str]

    @classmethod
    def from_domain(cls, option: RouteOption) -> "RouteOptionResponse":
        """从领域物流方案创建 API 响应。"""
        return cls(
            carrier=option.carrier,
            service=option.service,
            cost=option.cost.amount,
            currency=option.cost.currency,
            estimated_days=option.estimated_days,
            risk_score=option.risk_score.value,
            risk_label=option.risk_score.label,
            score=option.score,
            reasons=option.reasons or [],
        )


class RecommendationResponse(BaseModel):
    """物流推荐响应模型，用于返回最优和备选方案。"""

    best_option: RouteOptionResponse | None
    alternatives: list[RouteOptionResponse]

    @classmethod
    def from_domain(cls, result: RecommendationResult) -> "RecommendationResponse":
        """从领域推荐结果创建 API 响应。"""
        options = [RouteOptionResponse.from_domain(item) for item in result.options]
        best = options[0] if options else None
        return cls(best_option=best, alternatives=options[1:])


class TrackingResponse(BaseModel):
    """物流轨迹响应模型，用于返回最新状态和异常提示。"""

    tracking_no: str
    carrier: str
    status: str
    latest_location: str
    alerts: list[str]

    @classmethod
    def from_domain(cls, result: TrackingResult) -> "TrackingResponse":
        """从领域轨迹结果创建 API 响应。"""
        return cls(
            tracking_no=result.status.tracking_no,
            carrier=result.status.carrier,
            status=result.status.status,
            latest_location=result.status.latest_location,
            alerts=result.alerts,
        )


class InventoryForecastResponse(BaseModel):
    """库存预测响应模型，用于返回需求量和补货建议。"""

    sku: str
    region: str
    forecast_days: int
    predicted_units: int
    reorder_units: int
    reasons: list[str]

    @classmethod
    def from_domain(cls, result: InventoryForecast) -> "InventoryForecastResponse":
        """从领域库存预测结果创建 API 响应。"""
        return cls(**result.__dict__)


class ProfitResponse(BaseModel):
    """利润计算响应模型，用于返回毛利、净利和敏感项。"""

    sku: str
    gross_profit: Decimal
    net_profit: Decimal
    profit_margin: Decimal
    risk_items: list[str]

    @classmethod
    def from_domain(cls, result: ProfitResult) -> "ProfitResponse":
        """从领域利润结果创建 API 响应。"""
        return cls(
            sku=result.sku,
            gross_profit=result.gross_profit.amount,
            net_profit=result.net_profit.amount,
            profit_margin=result.profit_margin,
            risk_items=result.risk_items,
        )


class AssistantResponse(BaseModel):
    """AI 助手响应模型，用于返回回答、证据和下一步动作。"""

    answer: str
    citations: list[str]
    next_actions: list[str]

    @classmethod
    def from_domain(cls, result: AssistantAnswer) -> "AssistantResponse":
        """从领域 AI 助手结果创建 API 响应。"""
        return cls(**result.__dict__)
