from fastapi import APIRouter

from app.api.dependencies import ContainerDep
from app.api.schemas.requests import OrderRequest
from app.api.schemas.responses import RecommendationResponse

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.post("/recommend", response_model=RecommendationResponse)
async def recommend_shipping(
    request: OrderRequest,
    container: ContainerDep,
) -> RecommendationResponse:
    """根据订单、预算和时效要求推荐跨境物流方案。"""
    result = await container.recommend_shipping.execute(request.to_domain())
    return RecommendationResponse.from_domain(result)
