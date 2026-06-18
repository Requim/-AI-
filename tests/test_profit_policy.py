from decimal import Decimal

from app.domain.entities.profit import ProfitInput
from app.domain.policies.profit_policy import ProfitPolicy
from app.domain.value_objects.money import Money


def test_profit_policy_calculates_net_profit() -> None:
    """验证利润规则能正确计算净利。"""
    request = ProfitInput(
        sku="SKU-1",
        revenue=Money(Decimal("100")),
        product_cost=Money(Decimal("30")),
        shipping_cost=Money(Decimal("12")),
        storage_fee=Money(Decimal("3")),
        platform_fee=Money(Decimal("10")),
        tax=Money(Decimal("5")),
        return_rate=Decimal("0.05"),
    )
    result = ProfitPolicy().calculate(request)
    assert result.net_profit.amount == Decimal("35.00")
    assert result.profit_margin == Decimal("0.3500")
