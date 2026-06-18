from decimal import Decimal

from app.domain.entities.profit import ProfitInput, ProfitResult
from app.domain.value_objects.money import Money


class ProfitPolicy:
    """利润计算规则，用于汇总成本、净利和风险项。"""

    def calculate(self, request: ProfitInput) -> ProfitResult:
        """计算指定 SKU 的利润结果。"""
        gross_profit = request.revenue.subtract(request.product_cost)
        total_cost = self._total_cost(request)
        net_profit = request.revenue.subtract(total_cost)
        margin = self._margin(net_profit.amount, request.revenue.amount)
        risk_items = self._risk_items(request, margin)
        return ProfitResult(request.sku, gross_profit, net_profit, margin, risk_items)

    def _total_cost(self, request: ProfitInput) -> Money:
        costs = [
            request.product_cost,
            request.shipping_cost,
            request.storage_fee,
            request.platform_fee,
            request.tax,
            request.revenue.multiply(request.return_rate),
        ]
        return Money.sum(costs, request.revenue.currency)

    def _margin(self, net_profit: Decimal, revenue: Decimal) -> Decimal:
        return Decimal("0") if revenue == 0 else (net_profit / revenue).quantize(Decimal("0.0001"))

    def _risk_items(self, request: ProfitInput, margin: Decimal) -> list[str]:
        rules = [self._low_margin, self._high_return_rate, self._high_shipping_cost]
        return [item for rule in rules if (item := rule(request, margin))]

    def _low_margin(self, request: ProfitInput, margin: Decimal) -> str | None:
        return "净利率低于 10%，建议调整售价或物流渠道。" if margin < Decimal("0.1") else None

    def _high_return_rate(self, request: ProfitInput, margin: Decimal) -> str | None:
        if request.return_rate <= Decimal("0.08"):
            return None
        return "退货率较高，建议排查商品质量或物流破损。"

    def _high_shipping_cost(self, request: ProfitInput, margin: Decimal) -> str | None:
        ratio = request.shipping_cost.amount / request.revenue.amount
        return "运费占收入比例较高，建议切换经济渠道。" if ratio > Decimal("0.25") else None
