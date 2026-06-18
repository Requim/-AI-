from dataclasses import dataclass

from app.application.use_cases.ask_assistant import AskAssistantUseCase
from app.application.use_cases.calculate_profit import CalculateProfitUseCase
from app.application.use_cases.predict_inventory import PredictInventoryUseCase
from app.application.use_cases.recommend_shipping import RecommendShippingUseCase
from app.application.use_cases.update_tracking_status import UpdateTrackingStatusUseCase
from app.config.settings import Settings, get_settings
from app.domain.policies.anomaly_policy import AnomalyPolicy
from app.domain.policies.profit_policy import ProfitPolicy
from app.domain.ports.carrier_gateway import CarrierGateway
from app.domain.ports.llm_gateway import LLMGateway
from app.domain.ports.ml_predictor import MLPredictor
from app.domain.ports.route_optimizer import RouteOptimizer
from app.infrastructure.carriers.external_carriers import build_real_carriers
from app.infrastructure.carriers.mock_carrier import build_mock_carriers
from app.infrastructure.llm.simple_assistant import SimpleAssistantGateway
from app.infrastructure.ml.rule_based_predictor import RuleBasedPredictor
from app.infrastructure.optimization.heuristic_route_optimizer import HeuristicRouteOptimizer


@dataclass(frozen=True)
class AppContainer:
    """应用容器，集中保存所有用例实例。"""

    recommend_shipping: RecommendShippingUseCase
    update_tracking: UpdateTrackingStatusUseCase
    predict_inventory: PredictInventoryUseCase
    calculate_profit: CalculateProfitUseCase
    ask_assistant: AskAssistantUseCase


def build_container() -> AppContainer:
    """构建默认应用容器，根据配置注入外部服务实现。"""
    settings = get_settings()
    carriers = build_carriers(settings)
    predictor = build_predictor(settings)
    optimizer = build_optimizer(settings)
    anomaly_policy = AnomalyPolicy()
    profit_policy = ProfitPolicy()
    assistant = build_assistant(settings)
    return AppContainer(
        recommend_shipping=RecommendShippingUseCase(carriers, optimizer, predictor),
        update_tracking=UpdateTrackingStatusUseCase(carriers, anomaly_policy),
        predict_inventory=PredictInventoryUseCase(predictor),
        calculate_profit=CalculateProfitUseCase(profit_policy),
        ask_assistant=AskAssistantUseCase(assistant),
    )


def build_carriers(settings: Settings) -> list[CarrierGateway]:
    """根据承运商模式创建 Mock、真实或混合承运商适配器。"""
    if settings.carrier_mode == "real":
        return build_real_carriers(settings)
    if settings.carrier_mode == "mixed":
        return [*build_mock_carriers(), *build_real_carriers(settings)]
    return list(build_mock_carriers())


def build_predictor(settings: Settings) -> MLPredictor:
    """创建预测器，真实模型不可用时使用规则预测器兜底。"""
    return RuleBasedPredictor()


def build_optimizer(settings: Settings) -> RouteOptimizer:
    """创建路线优化器，后续可替换为 OR-Tools 约束优化实现。"""
    return HeuristicRouteOptimizer()


def build_assistant(settings: Settings) -> LLMGateway:
    """创建 AI 助手网关，后续可切换为 RAG/LLM 实现。"""
    return SimpleAssistantGateway()
