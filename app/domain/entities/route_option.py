from dataclasses import dataclass, replace
from decimal import Decimal

from app.domain.value_objects.money import Money
from app.domain.value_objects.risk_score import RiskScore


@dataclass(frozen=True)
class RouteOption:
    """物流方案实体，保存承运商、服务、成本、时效和风险。"""

    carrier: str
    service: str
    cost: Money
    estimated_days: int
    risk_score: RiskScore
    score: Decimal = Decimal("0")
    reasons: list[str] | None = None

    def with_risk(self, risk_score: RiskScore) -> "RouteOption":
        """返回带有新风险评分的物流方案。"""
        return replace(self, risk_score=risk_score)

    def with_score(self, score: Decimal, reasons: list[str]) -> "RouteOption":
        """返回带有推荐分和解释原因的物流方案。"""
        return replace(self, score=score, reasons=reasons)
