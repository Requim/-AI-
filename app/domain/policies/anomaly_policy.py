from app.domain.entities.tracking import TrackingStatus


class AnomalyPolicy:
    """物流异常检测规则，用于识别延误、丢件和未知轨迹。"""

    def detect(self, status: TrackingStatus) -> list[str]:
        """根据轨迹状态返回异常预警列表。"""
        rules = [
            self._unknown_tracking,
            self._delay_risk,
            self._damage_risk,
        ]
        return [alert for rule in rules if (alert := rule(status))]

    def _unknown_tracking(self, status: TrackingStatus) -> str | None:
        return "未查询到有效轨迹，建议检查单号或承运商。 " if status.status == "UNKNOWN" else None

    def _delay_risk(self, status: TrackingStatus) -> str | None:
        return "当前轨迹存在清关或派送延误风险。" if status.status == "DELAYED" else None

    def _damage_risk(self, status: TrackingStatus) -> str | None:
        if status.status != "EXCEPTION":
            return None
        return "承运商反馈包裹异常，建议准备补发或退款预案。"
