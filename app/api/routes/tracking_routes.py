from fastapi import APIRouter

from app.api.dependencies import ContainerDep
from app.api.schemas.responses import TrackingResponse

router = APIRouter(prefix="/tracking", tags=["tracking"])


@router.get("/{tracking_no}", response_model=TrackingResponse)
async def get_tracking(
    tracking_no: str,
    container: ContainerDep,
) -> TrackingResponse:
    """根据物流单号查询最新轨迹状态和异常预警。"""
    result = await container.update_tracking.execute(tracking_no)
    return TrackingResponse.from_domain(result)
