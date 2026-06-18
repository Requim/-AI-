from dataclasses import dataclass


@dataclass(frozen=True)
class ModelInfo:
    """模型元数据，保存模型名称、版本和用途。"""

    name: str
    version: str
    purpose: str


class InMemoryModelRegistry:
    """内存模型注册表，用于开发阶段管理模型元数据。"""

    def list_models(self) -> list[ModelInfo]:
        """返回当前可用模型列表。"""
        return [
            ModelInfo("delay-risk-rules", "0.1.0", "物流延误风险预测"),
            ModelInfo("demand-rules", "0.1.0", "库存需求预测"),
        ]
