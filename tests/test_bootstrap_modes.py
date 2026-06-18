from app.bootstrap import build_carriers
from app.config.settings import Settings
from app.infrastructure.carriers.real_carrier import RealCarrierGateway


def test_build_carriers_defaults_to_mock() -> None:
    """验证默认承运商模式使用 Mock。"""
    carriers = build_carriers(Settings())
    assert len(carriers) == 3


def test_build_carriers_uses_real_when_key_exists() -> None:
    """验证 real 模式会按 API Key 创建真实承运商。"""
    settings = Settings(carrier_mode="real", shippo_api_key="token")
    carriers = build_carriers(settings)
    assert len(carriers) == 1
    assert isinstance(carriers[0], RealCarrierGateway)


def test_build_carriers_supports_mixed_mode() -> None:
    """验证 mixed 模式会同时返回 Mock 和真实承运商。"""
    settings = Settings(carrier_mode="mixed", shippo_api_key="token")
    carriers = build_carriers(settings)
    assert len(carriers) == 4
