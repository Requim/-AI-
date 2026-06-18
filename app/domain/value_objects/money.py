from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    """金额值对象，统一保存数值和币种。"""

    amount: Decimal
    currency: str = "USD"

    def add(self, other: "Money") -> "Money":
        """返回两个同币种金额相加后的结果。"""
        self._ensure_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: "Money") -> "Money":
        """返回两个同币种金额相减后的结果。"""
        self._ensure_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def multiply(self, ratio: Decimal) -> "Money":
        """返回金额乘以比例后的结果。"""
        return Money((self.amount * ratio).quantize(Decimal("0.01")), self.currency)

    @classmethod
    def sum(cls, items: list["Money"], currency: str) -> "Money":
        """按指定币种汇总多个金额。"""
        total = Decimal("0")
        for item in items:
            if item.currency != currency:
                raise ValueError("金额币种不一致")
            total += item.amount
        return cls(total, currency)

    def _ensure_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError("金额币种不一致")
