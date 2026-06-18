from decimal import Decimal

from sqlalchemy.orm import Session

from app.domain.entities.inventory import InventoryForecast
from app.domain.entities.order import Order
from app.domain.entities.profit import ProfitResult
from app.domain.entities.recommendation import RecommendationResult
from app.domain.entities.route_option import RouteOption
from app.domain.entities.tracking import TrackingResult
from app.infrastructure.db.models import (
    InventoryForecastModel,
    OrderModel,
    ProfitResultModel,
    ShipmentModel,
    TaskStatusModel,
    TrackingEventModel,
)


class SqlAlchemyOrderRepository:
    """SQLAlchemy 订单仓储实现。"""

    def __init__(self, session: Session) -> None:
        """初始化订单仓储。"""
        self._session = session

    def save(self, order: Order) -> None:
        """保存订单核心信息。"""
        self._session.add(
            OrderModel(
                order_id=order.order_id,
                sku=order.sku,
                quantity=order.quantity,
                destination=order.destination.__dict__,
                package=_stringify(order.package.__dict__),
                requirement=_stringify(order.requirement.__dict__),
            )
        )


class SqlAlchemyRecommendationRepository:
    """SQLAlchemy 物流推荐仓储实现。"""

    def __init__(self, session: Session) -> None:
        """初始化物流推荐仓储。"""
        self._session = session

    def save(self, order_id: str, result: RecommendationResult) -> None:
        """保存订单对应的物流推荐结果。"""
        self._session.add_all([self._model(order_id, option) for option in result.options])

    def _model(self, order_id: str, option: RouteOption) -> ShipmentModel:
        return ShipmentModel(
            order_id=order_id,
            carrier=option.carrier,
            service=option.service,
            cost=option.cost.amount,
            estimated_days=option.estimated_days,
            risk_score=option.risk_score.value,
            reasons=option.reasons or [],
        )


class SqlAlchemyTrackingRepository:
    """SQLAlchemy 物流轨迹仓储实现。"""

    def __init__(self, session: Session) -> None:
        """初始化物流轨迹仓储。"""
        self._session = session

    def save(self, result: TrackingResult) -> None:
        """保存物流轨迹状态和异常预警。"""
        status = result.status
        self._session.add(
            TrackingEventModel(
                tracking_no=status.tracking_no,
                carrier=status.carrier,
                status=status.status,
                latest_location=status.latest_location,
                alerts=result.alerts,
            )
        )


class SqlAlchemyInventoryForecastRepository:
    """SQLAlchemy 库存预测仓储实现。"""

    def __init__(self, session: Session) -> None:
        """初始化库存预测仓储。"""
        self._session = session

    def save(self, forecast: InventoryForecast) -> None:
        """保存库存预测结果。"""
        self._session.add(InventoryForecastModel(**forecast.__dict__))


class SqlAlchemyProfitResultRepository:
    """SQLAlchemy 利润结果仓储实现。"""

    def __init__(self, session: Session) -> None:
        """初始化利润结果仓储。"""
        self._session = session

    def save(self, result: ProfitResult) -> None:
        """保存利润计算结果。"""
        self._session.add(
            ProfitResultModel(
                sku=result.sku,
                gross_profit=result.gross_profit.amount,
                net_profit=result.net_profit.amount,
                profit_margin=result.profit_margin,
                risk_items=result.risk_items,
            )
        )


class SqlAlchemyTaskStatusRepository:
    """SQLAlchemy 任务状态仓储实现。"""

    def __init__(self, session: Session) -> None:
        """初始化任务状态仓储。"""
        self._session = session

    def save(self, task_name: str, status: str, message: str = "") -> None:
        """保存后台任务状态。"""
        self._session.add(TaskStatusModel(task_name=task_name, status=status, message=message))


def _stringify(values: dict[str, object]) -> dict[str, str]:
    return {key: _value_to_string(value) for key, value in values.items()}


def _value_to_string(value: object) -> str:
    if isinstance(value, Decimal):
        return str(value)
    return str(value)
