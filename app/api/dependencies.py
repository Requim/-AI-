from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.bootstrap import AppContainer, build_container


@lru_cache
def get_container() -> AppContainer:
    """获取应用容器，供 FastAPI 依赖注入使用。"""
    return build_container()


ContainerDep = Annotated[AppContainer, Depends(get_container)]
