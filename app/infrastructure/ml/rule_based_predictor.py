from app.domain.entities.inventory import InventoryForecast
from app.domain.entities.ml import MarketContext
from app.domain.entities.route_option import RouteOption
from app.domain.value_objects.risk_score import RiskScore


class RuleBasedPredictor:
    """规则型预测器，用于在真实模型接入前提供稳定输出。"""

    def predict_delay_risk(self, option: RouteOption, context: MarketContext) -> RiskScore:
        """根据区域、时效和服务类型预测延误风险。"""
        score = 10
        score += 25 if option.estimated_days > 8 else 0
        score += 20 if context.region.upper() in {"AK", "HI", "REMOTE"} else 0
        score += 15 if option.service.lower() == "economy" else 0
        return RiskScore.clamp(score)

    def predict_demand(self, sku: str, days: int, context: MarketContext) -> InventoryForecast:
        """根据历史销量预测未来需求。"""
        daily_average = self._daily_average(context.sales_history)
        predicted_units = max(1, int(daily_average * days))
        reasons = self._demand_reasons(context.sales_history, daily_average)
        return InventoryForecast(sku, context.region, days, predicted_units, 0, reasons)

    def _daily_average(self, sales_history: list[int]) -> float:
        if not sales_history:
            return 1.0
        return sum(sales_history) / len(sales_history)

    def _demand_reasons(self, sales_history: list[int], daily_average: float) -> list[str]:
        if not sales_history:
            return ["缺少历史销量，使用保守日均 1 件。"]
        return [f"按历史日均 {daily_average:.1f} 件预测。"]
