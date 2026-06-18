from dataclasses import dataclass

from app.domain.value_objects.address import Address
from app.domain.value_objects.money import Money
from app.domain.value_objects.package import Package


@dataclass(frozen=True)
class ShippingRequirement:
    """物流要求，保存最大时效、预算和偏好渠道。"""

    max_days: int
    max_budget: Money
    preferred_channels: list[str]


@dataclass(frozen=True)
class Order:
    """订单实体，保存推荐物流所需的核心订单信息。"""

    order_id: str
    sku: str
    quantity: int
    destination: Address
    package: Package
    requirement: ShippingRequirement
