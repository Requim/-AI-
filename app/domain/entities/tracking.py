from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class TrackingStatus:
    """物流轨迹状态，保存单号、承运商、位置和状态。"""

    tracking_no: str
    carrier: str
    status: str
    latest_location: str
    updated_at: datetime

    @classmethod
    def unknown(cls, tracking_no: str) -> "TrackingStatus":
        """创建未知轨迹状态。"""
        return cls(tracking_no, "unknown", "UNKNOWN", "unknown", datetime.now(UTC))


@dataclass(frozen=True)
class TrackingResult:
    """物流轨迹结果，保存状态和异常预警。"""

    status: TrackingStatus
    alerts: list[str]
