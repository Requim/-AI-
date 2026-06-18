from dataclasses import dataclass

from app.application.use_cases.ask_assistant import AskAssistantUseCase
from app.application.use_cases.calculate_profit import CalculateProfitUseCase
from app.application.use_cases.predict_inventory import PredictInventoryUseCase
from app.application.use_cases.recommend_shipping import RecommendShippingUseCase
from app.application.use_cases.update_tracking_status import UpdateTrackingStatusUseCase
from app.domain.policies.anomaly_policy import AnomalyPolicy
from app.domain.policies.profit_policy import ProfitPolicy
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
    """构建默认应用容器，注入 Mock 外部服务实现。"""
    carriers = build_mock_carriers()
    predictor = RuleBasedPredictor()
    optimizer = HeuristicRouteOptimizer()
    anomaly_policy = AnomalyPolicy()
    profit_policy = ProfitPolicy()
    assistant = SimpleAssistantGateway()
    return AppContainer(
        recommend_shipping=RecommendShippingUseCase(carriers, optimizer, predictor),
        update_tracking=UpdateTrackingStatusUseCase(carriers, anomaly_policy),
        predict_inventory=PredictInventoryUseCase(predictor),
        calculate_profit=CalculateProfitUseCase(profit_policy),
        ask_assistant=AskAssistantUseCase(assistant),
    )
