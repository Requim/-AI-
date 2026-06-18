from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Package:
    """包裹值对象，保存重量和尺寸。"""

    weight_kg: Decimal
    length_cm: Decimal
    width_cm: Decimal
    height_cm: Decimal

    @property
    def volume_cbm(self) -> Decimal:
        """计算包裹体积，单位为立方米。"""
        return self.length_cm * self.width_cm * self.height_cm / Decimal("1000000")
