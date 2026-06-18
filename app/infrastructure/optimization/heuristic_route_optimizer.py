from decimal import Decimal

from app.domain.entities.order import Order
from app.domain.entities.route_option import RouteOption


class HeuristicRouteOptimizer:
    """启发式路线优化器，后续可替换为 OR-Tools 实现。"""

    def rank(self, order: Order, options: list[RouteOption]) -> list[RouteOption]:
        """根据成本、时效和风险对物流方案排序。"""
        scored = [self._score_option(order, option) for option in options]
        return sorted(scored, key=lambda item: item.score)

    def _score_option(self, order: Order, option: RouteOption) -> RouteOption:
        budget_penalty = self._budget_penalty(order, option)
        speed_penalty = self._speed_penalty(order, option)
        risk_penalty = Decimal(option.risk_score.value) / Decimal("100")
        score = option.cost.amount + budget_penalty + speed_penalty + risk_penalty
        reasons = self._reasons(order, option, budget_penalty, speed_penalty)
        return option.with_score(score.quantize(Decimal("0.01")), reasons)

    def _budget_penalty(self, order: Order, option: RouteOption) -> Decimal:
        over_budget = option.cost.amount - order.requirement.max_budget.amount
        return max(Decimal("0"), over_budget * Decimal("2"))

    def _speed_penalty(self, order: Order, option: RouteOption) -> Decimal:
        over_days = option.estimated_days - order.requirement.max_days
        return max(Decimal("0"), Decimal(over_days) * Decimal("3"))

    def _reasons(
        self,
        order: Order,
        option: RouteOption,
        budget_penalty: Decimal,
        speed_penalty: Decimal,
    ) -> list[str]:
        reasons = [f"{option.carrier} {option.service} 预计 {option.estimated_days} 天。"]
        reasons.append(f"风险等级：{option.risk_score.label}。")
        reasons.extend(self._penalty_reasons(budget_penalty, speed_penalty))
        return reasons

    def _penalty_reasons(self, budget_penalty: Decimal, speed_penalty: Decimal) -> list[str]:
        reasons = []
        if budget_penalty > 0:
            reasons.append("费用超过预算，已加入成本惩罚。")
        if speed_penalty > 0:
            reasons.append("时效超过要求，已加入时效惩罚。")
        return reasons
