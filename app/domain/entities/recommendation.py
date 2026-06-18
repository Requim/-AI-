from dataclasses import dataclass

from app.domain.entities.route_option import RouteOption


@dataclass(frozen=True)
class RecommendationResult:
    """物流推荐结果，保存排序后的所有候选方案。"""

    options: list[RouteOption]
