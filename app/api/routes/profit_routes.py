from fastapi import APIRouter

from app.api.dependencies import ContainerDep
from app.api.schemas.requests import ProfitRequest
from app.api.schemas.responses import ProfitResponse

router = APIRouter(prefix="/profit", tags=["profit"])


@router.post("/calculate", response_model=ProfitResponse)
async def calculate_profit(
    request: ProfitRequest,
    container: ContainerDep,
) -> ProfitResponse:
    """根据商品、物流、平台、关税和退货成本计算利润。"""
    result = container.calculate_profit.execute(request.to_domain())
    return ProfitResponse.from_domain(result)
