from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    """地址值对象，保存国家、地区、城市和邮编。"""

    country: str
    region: str
    city: str
    postal_code: str
