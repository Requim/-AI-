from app.domain.entities.assistant import AssistantAnswer, AssistantContext
from app.domain.ports.llm_gateway import LLMGateway


class AskAssistantUseCase:
    """AI 助手用例，负责组织上下文并调用语言模型网关。"""

    def __init__(self, llm_gateway: LLMGateway) -> None:
        """初始化 AI 助手用例。"""
        self._llm_gateway = llm_gateway

    async def execute(self, context: AssistantContext) -> AssistantAnswer:
        """执行 AI 助手问答。"""
        return await self._llm_gateway.answer(context.question, context)
