from dataclasses import dataclass
from decimal import Decimal

from app.domain.value_objects.money import Money


@dataclass(frozen=True)
class ProfitInput:
    """利润计算输入，保存收入和各类成本。"""

    sku: str
    revenue: Money
    product_cost: Money
    shipping_cost: Money
    storage_fee: Money
    platform_fee: Money
    tax: Money
    return_rate: Decimal


@dataclass(frozen=True)
class ProfitResult:
    """利润计算结果，保存毛利、净利、利润率和风险项。"""

    sku: str
    gross_profit: Money
    net_profit: Money
    profit_margin: Decimal
    risk_items: list[str]
