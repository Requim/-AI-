from app.config.settings import Settings
from app.domain.ports.carrier_gateway import CarrierGateway
from app.infrastructure.carriers.real_carrier import RealCarrierConfig, RealCarrierGateway
from app.infrastructure.http.client import ExternalHttpClient, HttpClientConfig


def build_real_carriers(settings: Settings) -> list[CarrierGateway]:
    """根据 API Key 创建真实承运商适配器列表。"""
    client = ExternalHttpClient(
        HttpClientConfig(settings.carrier_timeout_seconds, settings.carrier_retry_count)
    )
    configs = _carrier_configs(settings)
    return [RealCarrierGateway(config, client) for config in configs if config.api_key]


def _carrier_configs(settings: Settings) -> list[RealCarrierConfig]:
    return [
        RealCarrierConfig("Shippo", settings.shippo_api_key, "https://api.goshippo.com"),
        RealCarrierConfig("DHL", settings.dhl_api_key, "https://api-eu.dhl.com"),
        RealCarrierConfig("FedEx", settings.fedex_api_key, "https://apis.fedex.com"),
        RealCarrierConfig("UPS", settings.ups_api_key, "https://onlinetools.ups.com"),
        RealCarrierConfig("AfterShip", settings.aftership_api_key, "https://api.aftership.com"),
    ]
