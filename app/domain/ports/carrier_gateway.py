from typing import Protocol

from app.domain.entities.quote import QuoteRequest
from app.domain.entities.route_option import RouteOption
from app.domain.entities.tracking import TrackingStatus


class CarrierGateway(Protocol):
    """物流承运商接口，用于获取报价和轨迹信息。"""

    async def get_quote(self, request: QuoteRequest) -> list[RouteOption]:
        """根据订单包裹、地址和时效要求获取物流报价。"""
        ...

    async def get_tracking(self, tracking_no: str) -> TrackingStatus:
        """根据物流单号获取最新轨迹状态。"""
        ...
