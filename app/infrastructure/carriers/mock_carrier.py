from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

from app.domain.entities.quote import QuoteRequest
from app.domain.entities.route_option import RouteOption
from app.domain.entities.tracking import TrackingStatus
from app.domain.value_objects.money import Money
from app.domain.value_objects.risk_score import RiskScore


@dataclass(frozen=True)
class MockCarrierGateway:
    """Mock 承运商适配器，用于开发和测试阶段模拟报价与轨迹。"""

    carrier: str
    base_cost: Decimal
    base_days: int
    service: str

    async def get_quote(self, request: QuoteRequest) -> list[RouteOption]:
        """根据包裹重量和目的地生成模拟报价。"""
        package = request.order.package
        cost = self.base_cost + package.weight_kg * Decimal("1.8")
        option = RouteOption(
            carrier=self.carrier,
            service=self.service,
            cost=Money(cost.quantize(Decimal("0.01"))),
            estimated_days=self.base_days,
            risk_score=RiskScore(0),
        )
        return [option]

    async def get_tracking(self, tracking_no: str) -> TrackingStatus:
        """返回模拟轨迹状态，用于本地联调。"""
        status = self._status_for_tracking_no(tracking_no)
        return TrackingStatus(tracking_no, self.carrier, status, "Los Angeles", datetime.now(UTC))

    def _status_for_tracking_no(self, tracking_no: str) -> str:
        if tracking_no.endswith("9"):
            return "DELAYED"
        if tracking_no.endswith("8"):
            return "EXCEPTION"
        return "IN_TRANSIT"


def build_mock_carriers() -> list[MockCarrierGateway]:
    """创建默认 Mock 承运商列表。"""
    return [
        MockCarrierGateway("4PX", Decimal("8.50"), 9, "Economy"),
        MockCarrierGateway("Shippo", Decimal("13.20"), 6, "Standard"),
        MockCarrierGateway("AfterShip", Decimal("21.80"), 3, "Express"),
    ]
