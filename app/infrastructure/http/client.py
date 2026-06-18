import asyncio
from dataclasses import dataclass
from typing import Any

import httpx


class ExternalServiceError(RuntimeError):
    """外部服务错误，统一包装承运商、模型和 LLM 调用失败。"""


@dataclass(frozen=True)
class HttpClientConfig:
    """HTTP 客户端配置，用于控制超时和重试次数。"""

    timeout_seconds: float
    retry_count: int


class ExternalHttpClient:
    """外部 HTTP 客户端，统一处理超时、重试和敏感信息脱敏。"""

    def __init__(self, config: HttpClientConfig) -> None:
        """初始化 HTTP 客户端。"""
        self._config = config

    async def get_json(
        self,
        url: str,
        headers: dict[str, str],
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """发送 GET 请求并返回 JSON 响应。"""
        return await self._request_json("GET", url, headers, params=params)

    async def post_json(
        self,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """发送 POST 请求并返回 JSON 响应。"""
        return await self._request_json("POST", url, headers, json=payload)

    async def _request_json(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        **kwargs: Any,
    ) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(self._config.retry_count + 1):
            try:
                return await self._send(method, url, headers, **kwargs)
            except (httpx.HTTPError, ValueError) as exc:
                last_error = exc
                await self._backoff(attempt)
        raise ExternalServiceError(f"外部服务请求失败：{self._safe_url(url)}") from last_error

    async def _send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        **kwargs: Any,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self._config.timeout_seconds) as client:
            response = await client.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise ValueError("外部服务响应不是 JSON 对象")
            return data

    async def _backoff(self, attempt: int) -> None:
        if attempt < self._config.retry_count:
            await asyncio.sleep(0.2 * (attempt + 1))

    def _safe_url(self, url: str) -> str:
        return url.split("?")[0]
