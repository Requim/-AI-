from fastapi import APIRouter

from app.api.dependencies import ContainerDep
from app.api.schemas.requests import InventoryForecastRequest
from app.api.schemas.responses import InventoryForecastResponse

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.post("/forecast", response_model=InventoryForecastResponse)
async def forecast_inventory(
    request: InventoryForecastRequest,
    container: ContainerDep,
) -> InventoryForecastResponse:
    """预测指定 SKU 在目标区域的未来需求和补货建议。"""
    result = container.predict_inventory.execute(request.to_domain())
    return InventoryForecastResponse.from_domain(result)
