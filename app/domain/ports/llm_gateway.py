from typing import Protocol

from app.domain.entities.assistant import AssistantAnswer, AssistantContext


class LLMGateway(Protocol):
    """AI 助手接口，用于基于业务上下文回答用户问题。"""

    async def answer(self, question: str, context: AssistantContext) -> AssistantAnswer:
        """基于订单、物流、库存和成本上下文生成回答。"""
        ...
