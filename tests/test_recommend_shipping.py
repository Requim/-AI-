from decimal import Decimal

import pytest

from app.api.schemas.requests import (
    AddressSchema,
    OrderRequest,
    PackageSchema,
    ShippingRequirementSchema,
)
from app.bootstrap import build_container


@pytest.mark.asyncio
async def test_recommend_shipping_returns_ranked_options() -> None:
    """验证物流推荐用例返回排序后的候选方案。"""
    order = OrderRequest(
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
    result = await build_container().recommend_shipping.execute(order)
    assert result.options
    assert result.options[0].score <= result.options[-1].score
