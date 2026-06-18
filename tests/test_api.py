from fastapi.testclient import TestClient

from app.main import app


def test_profit_api_returns_margin() -> None:
    """验证利润接口能返回净利率。"""
    client = TestClient(app)
    response = client.post(
        "/profit/calculate",
        json={
            "sku": "SKU-1",
            "revenue": "100",
            "product_cost": "30",
            "shipping_cost": "12",
            "storage_fee": "3",
            "platform_fee": "10",
            "tax": "5",
            "return_rate": "0.05",
        },
    )
    assert response.status_code == 200
    assert response.json()["profit_margin"] == "0.3500"
