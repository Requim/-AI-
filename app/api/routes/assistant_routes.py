from fastapi import APIRouter

from app.api.dependencies import ContainerDep
from app.api.schemas.requests import AssistantRequest
from app.api.schemas.responses import AssistantResponse

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/ask", response_model=AssistantResponse)
async def ask_assistant(
    request: AssistantRequest,
    container: ContainerDep,
) -> AssistantResponse:
    """接收自然语言问题，返回基于业务上下文的 AI 助手回答。"""
    result = await container.ask_assistant.execute(request.to_context())
    return AssistantResponse.from_domain(result)
