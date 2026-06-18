from dataclasses import dataclass


@dataclass(frozen=True)
class RiskScore:
    """风险评分值对象，分值范围为 0 到 100。"""

    value: int

    @property
    def label(self) -> str:
        """返回风险等级中文标签。"""
        if self.value >= 70:
            return "高风险"
        if self.value >= 35:
            return "中风险"
        return "低风险"

    @classmethod
    def clamp(cls, value: int) -> "RiskScore":
        """把任意整数裁剪为合法风险评分。"""
        return cls(max(0, min(100, value)))
