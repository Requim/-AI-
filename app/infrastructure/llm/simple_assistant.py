from app.domain.entities.assistant import AssistantAnswer, AssistantContext


class SimpleAssistantGateway:
    """本地 AI 助手适配器，用规则模板模拟 RAG/LLM 输出。"""

    async def answer(self, question: str, context: AssistantContext) -> AssistantAnswer:
        """根据问题和上下文生成可解释的业务回答。"""
        topic = self._topic(question)
        answer = self._answer_for_topic(topic, context)
        return AssistantAnswer(
            answer=answer,
            citations=["mock://orders", "mock://logistics-rules"],
            next_actions=self._next_actions(topic),
        )

    def _topic(self, question: str) -> str:
        if "库存" in question or "补货" in question:
            return "inventory"
        if "利润" in question or "成本" in question:
            return "profit"
        return "shipping"

    def _answer_for_topic(self, topic: str, context: AssistantContext) -> str:
        answers = {
            "inventory": f"SKU {context.sku or '未知'} 建议结合 30 天销量和物流周期计算安全库存。",
            "profit": "建议优先检查运费占比、平台费和退货率，它们通常最影响净利。",
            "shipping": "建议比较经济、标准、快速渠道，并同时关注清关延误风险。",
        }
        return answers[topic]

    def _next_actions(self, topic: str) -> list[str]:
        actions = {
            "inventory": ["调用库存预测接口", "检查 FBA 入仓周期"],
            "profit": ["调用利润计算接口", "比较不同物流渠道成本"],
            "shipping": ["调用物流推荐接口", "订阅轨迹异常预警"],
        }
        return actions[topic]
