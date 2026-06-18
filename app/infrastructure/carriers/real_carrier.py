from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Protocol

from app.domain.entities.quote import QuoteRequest
from app.domain.entities.route_option import RouteOption
from app.domain.entities.tracking import TrackingStatus
from app.domain.value_objects.money import Money
from app.domain.value_objects.risk_score import RiskScore
from app.infrastructure.http.client import ExternalServiceError


class CarrierHttpClient(Protocol):
    """承运商 HTTP 客户端协议，用于真实适配器和测试替身。"""

    async def get_json(
        self,
        url: str,
        headers: dict[str, str],
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """发送 GET 请求并返回 JSON 对象。"""
        ...

    async def post_json(
        self,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """发送 POST 请求并返回 JSON 对象。"""
        ...


@dataclass(frozen=True)
class RealCarrierConfig:
    """真实承运商配置，保存名称、凭据和 API 根地址。"""

    name: str
    api_key: str
    base_url: str


class RealCarrierGateway:
    """真实承运商适配器，统一封装报价和轨迹 API 调用。"""

    def __init__(self, config: RealCarrierConfig, client: CarrierHttpClient) -> None:
        """初始化真实承运商适配器。"""
        self._config = config
        self._client = client

    async def get_quote(self, request: QuoteRequest) -> list[RouteOption]:
        """请求真实承运商报价，并转换为领域物流方案。"""
        payload = self._quote_payload(request)
        data = await self._client.post_json(self._url("/rates"), self._headers(), payload)
        return [self._route_option(item) for item in self._items(data, "rates")]

    async def get_tracking(self, tracking_no: str) -> TrackingStatus:
        """请求真实承运商轨迹，并转换为领域轨迹状态。"""
        data = await self._client.get_json(
            self._url(f"/tracking/{tracking_no}"),
            self._headers(),
        )
        return self._tracking_status(tracking_no, data)

    def _quote_payload(self, request: QuoteRequest) -> dict[str, Any]:
        order = request.order
        return {
            "order_id": order.order_id,
            "destination": order.destination.__dict__,
            "package": order.package.__dict__,
            "max_days": order.requirement.max_days,
        }

    def _route_option(self, item: dict[str, Any]) -> RouteOption:
        return RouteOption(
            carrier=str(item.get("carrier", self._config.name)),
            service=str(item.get("service", "standard")),
            cost=Money(Decimal(str(item.get("cost", "0")))),
            estimated_days=int(item.get("estimated_days", 0)),
            risk_score=RiskScore.clamp(int(item.get("risk_score", 20))),
        )

    def _tracking_status(self, tracking_no: str, data: dict[str, Any]) -> TrackingStatus:
        return TrackingStatus(
            tracking_no=tracking_no,
            carrier=str(data.get("carrier", self._config.name)),
            status=str(data.get("status", "UNKNOWN")),
            latest_location=str(data.get("latest_location", "unknown")),
            updated_at=datetime.now(UTC),
        )

    def _items(self, data: dict[str, Any], key: str) -> list[dict[str, Any]]:
        items = data.get(key, [])
        if not isinstance(items, list):
            raise ExternalServiceError("外部承运商响应列表格式错误")
        return [item for item in items if isinstance(item, dict)]

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._config.api_key}"}

    def _url(self, path: str) -> str:
        return f"{self._config.base_url.rstrip('/')}{path}"
