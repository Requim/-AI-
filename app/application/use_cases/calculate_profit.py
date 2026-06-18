from app.domain.entities.profit import ProfitInput, ProfitResult
from app.domain.policies.profit_policy import ProfitPolicy


class CalculateProfitUseCase:
    """利润计算用例，负责调用利润规则并返回结果。"""

    def __init__(self, profit_policy: ProfitPolicy) -> None:
        """初始化利润计算用例。"""
        self._profit_policy = profit_policy

    def execute(self, request: ProfitInput) -> ProfitResult:
        """执行利润计算。"""
        return self._profit_policy.calculate(request)
