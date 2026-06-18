import asyncio
from collections.abc import Sequence

from app.domain.entities.tracking import TrackingResult, TrackingStatus
from app.domain.policies.anomaly_policy import AnomalyPolicy
from app.domain.ports.carrier_gateway import CarrierGateway


class UpdateTrackingStatusUseCase:
    """轨迹更新用例，负责查询承运商状态并检测异常。"""

    def __init__(self, carriers: Sequence[CarrierGateway], anomaly_policy: AnomalyPolicy) -> None:
        """初始化轨迹更新用例。"""
        self._carriers = list(carriers)
        self._anomaly_policy = anomaly_policy

    async def execute(self, tracking_no: str) -> TrackingResult:
        """执行轨迹查询和异常检测。"""
        status = await self._find_tracking_status(tracking_no)
        alerts = self._anomaly_policy.detect(status)
        return TrackingResult(status, alerts)

    async def _find_tracking_status(self, tracking_no: str) -> TrackingStatus:
        tasks = [carrier.get_tracking(tracking_no) for carrier in self._carriers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for item in results:
            if isinstance(item, TrackingStatus):
                return item
        return TrackingStatus.unknown(tracking_no)
