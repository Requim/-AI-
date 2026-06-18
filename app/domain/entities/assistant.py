from dataclasses import dataclass


@dataclass(frozen=True)
class AssistantContext:
    """AI 助手上下文，保存问题和可选业务定位信息。"""

    question: str
    order_id: str | None = None
    sku: str | None = None
    locale: str = "zh-CN"


@dataclass(frozen=True)
class AssistantAnswer:
    """AI 助手回答，保存答案、引用依据和后续动作。"""

    answer: str
    citations: list[str]
    next_actions: list[str]
