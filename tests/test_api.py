from fastapi.testclient import TestClient

from defai.api import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "DeFAI Analytics API",
        "status": "running",
    }

def test_dashboard_endpoint():
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "DeFAI Analytics Dashboard" in response.text
    assert "Total Transactions" in response.text
def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "defai_transactions_total" in response.text
    assert "defai_transactions_successful" in response.text
    assert "defai_transactions_failed" in response.text
