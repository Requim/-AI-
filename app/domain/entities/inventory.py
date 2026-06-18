from dataclasses import dataclass, replace


@dataclass(frozen=True)
class InventoryForecastRequest:
    """库存预测请求，保存 SKU、区域、预测天数和历史销量。"""

    sku: str
    region: str
    days: int
    lead_time_days: int
    sales_history: list[int]


@dataclass(frozen=True)
class InventoryForecast:
    """库存预测结果，保存预测销量、补货数量和原因。"""

    sku: str
    region: str
    forecast_days: int
    predicted_units: int
    reorder_units: int
    reasons: list[str]

    def with_reorder_units(self, lead_time_days: int) -> "InventoryForecast":
        """根据补货周期生成建议补货数量。"""
        daily_units = max(1, self.predicted_units // max(1, self.forecast_days))
        reorder_units = daily_units * lead_time_days
        return replace(self, reorder_units=reorder_units)
