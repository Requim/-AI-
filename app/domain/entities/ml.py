from dataclasses import dataclass, field


@dataclass(frozen=True)
class MarketContext:
    """市场上下文，保存区域、销量历史和促销标签。"""

    region: str
    sales_history: list[int] = field(default_factory=list)
    promotion_tags: list[str] = field(default_factory=list)
