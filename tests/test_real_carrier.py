from decimal import Decimal
from typing import Any

import pytest

from app.api.schemas.requests import (
    AddressSchema,
    OrderRequest,
    PackageSchema,
    ShippingRequirementSchema,
)
from app.domain.entities.order import Order
from app.domain.entities.quote import QuoteRequest
from app.infrastructure.carriers.real_carrier import RealCarrierConfig, RealCarrierGateway


class FakeHttpClient:
    """测试 HTTP 客户端，用于模拟真实承运商响应。"""

    async def post_json(
        self,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """返回模拟报价响应。"""
        return {"rates": [{"carrier": "Shippo", "service": "standard", "cost": "12.30"}]}

    async def get_json(
        self,
        url: str,
        headers: dict[str, str],
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """返回模拟轨迹响应。"""
        return {"carrier": "Shippo", "status": "IN_TRANSIT", "latest_location": "LA"}


@pytest.mark.asyncio
async def test_real_carrier_maps_quote_response() -> None:
    """验证真实承运商报价响应会转换为领域物流方案。"""
    gateway = _gateway()
    options = await gateway.get_quote(QuoteRequest(_order()))
    assert options[0].carrier == "Shippo"
    assert options[0].cost.amount == Decimal("12.30")


@pytest.mark.asyncio
async def test_real_carrier_maps_tracking_response() -> None:
    """验证真实承运商轨迹响应会转换为领域轨迹状态。"""
    gateway = _gateway()
    status = await gateway.get_tracking("T-1")
    assert status.status == "IN_TRANSIT"
    assert status.latest_location == "LA"


def _gateway() -> RealCarrierGateway:
    return RealCarrierGateway(
        RealCarrierConfig("Shippo", "token", "https://api"),
        FakeHttpClient(),
    )


def _order() -> Order:
    return OrderRequest(
        order_id="O-1",
        sku="SKU-1",
        quantity=1,
        destination=AddressSchema(country="US", region="CA", city="LA", postal_code="90001"),
        package=PackageSchema(
            weight_kg=Decimal("2"),
            length_cm=Decimal("20"),
            width_cm=Decimal("15"),
            height_cm=Decimal("10"),
        ),
        requirement=ShippingRequirementSchema(max_days=7, max_budget=Decimal("25")),
    ).to_domain()
