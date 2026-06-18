from decimal import Decimal

from pydantic import BaseModel, Field

from app.domain.entities.assistant import AssistantContext
from app.domain.entities.inventory import InventoryForecastRequest as DomainInventoryRequest
from app.domain.entities.order import Order, ShippingRequirement
from app.domain.entities.profit import ProfitInput
from app.domain.value_objects.address import Address
from app.domain.value_objects.money import Money
from app.domain.value_objects.package import Package


class AddressSchema(BaseModel):
    """地址请求模型，用于接收目的国家、地区、城市和邮编。"""

    country: str = Field(..., examples=["US"])
    region: str = Field(..., examples=["CA"])
    city: str = Field(..., examples=["Los Angeles"])
    postal_code: str = Field(..., examples=["90001"])

    def to_domain(self) -> Address:
        """转换为领域地址值对象。"""
        return Address(self.country, self.region, self.city, self.postal_code)


class PackageSchema(BaseModel):
    """包裹请求模型，用于接收重量和尺寸。"""

    weight_kg: Decimal = Field(..., gt=0)
    length_cm: Decimal = Field(..., gt=0)
    width_cm: Decimal = Field(..., gt=0)
    height_cm: Decimal = Field(..., gt=0)

    def to_domain(self) -> Package:
        """转换为领域包裹值对象。"""
        return Package(self.weight_kg, self.length_cm, self.width_cm, self.height_cm)


class ShippingRequirementSchema(BaseModel):
    """物流要求请求模型，用于接收预算、时效和渠道偏好。"""

    max_days: int = Field(..., gt=0)
    max_budget: Decimal = Field(..., gt=0)
    preferred_channels: list[str] = Field(default_factory=list)

    def to_domain(self) -> ShippingRequirement:
        """转换为领域物流要求。"""
        budget = Money(self.max_budget)
        return ShippingRequirement(self.max_days, budget, self.preferred_channels)


class OrderRequest(BaseModel):
    """订单请求模型，用于物流推荐入口。"""

    order_id: str
    sku: str
    quantity: int = Field(..., gt=0)
    destination: AddressSchema
    package: PackageSchema
    requirement: ShippingRequirementSchema

    def to_domain(self) -> Order:
        """转换为领域订单实体。"""
        return Order(
            order_id=self.order_id,
            sku=self.sku,
            quantity=self.quantity,
            destination=self.destination.to_domain(),
            package=self.package.to_domain(),
            requirement=self.requirement.to_domain(),
        )


class InventoryForecastRequest(BaseModel):
    """库存预测请求模型，用于接收销量、区域和补货周期。"""

    sku: str
    region: str
    days: int = Field(default=30, gt=0, le=90)
    lead_time_days: int = Field(default=10, gt=0)
    sales_history: list[int] = Field(default_factory=list)

    def to_domain(self) -> DomainInventoryRequest:
        """转换为领域库存预测请求。"""
        return DomainInventoryRequest(
            sku=self.sku,
            region=self.region,
            days=self.days,
            lead_time_days=self.lead_time_days,
            sales_history=self.sales_history,
        )


class ProfitRequest(BaseModel):
    """利润计算请求模型，用于接收收入和各类成本。"""

    sku: str
    revenue: Decimal = Field(..., gt=0)
    product_cost: Decimal = Field(..., ge=0)
    shipping_cost: Decimal = Field(..., ge=0)
    storage_fee: Decimal = Field(default=Decimal("0"), ge=0)
    platform_fee: Decimal = Field(default=Decimal("0"), ge=0)
    tax: Decimal = Field(default=Decimal("0"), ge=0)
    return_rate: Decimal = Field(default=Decimal("0"), ge=0, le=1)

    def to_domain(self) -> ProfitInput:
        """转换为领域利润计算输入。"""
        return ProfitInput(
            sku=self.sku,
            revenue=Money(self.revenue),
            product_cost=Money(self.product_cost),
            shipping_cost=Money(self.shipping_cost),
            storage_fee=Money(self.storage_fee),
            platform_fee=Money(self.platform_fee),
            tax=Money(self.tax),
            return_rate=self.return_rate,
        )


class AssistantRequest(BaseModel):
    """AI 助手请求模型，用于接收问题和业务上下文。"""

    question: str
    order_id: str | None = None
    sku: str | None = None
    locale: str = "zh-CN"

    def to_context(self) -> AssistantContext:
        """转换为领域 AI 助手上下文。"""
        return AssistantContext(self.question, self.order_id, self.sku, self.locale)
