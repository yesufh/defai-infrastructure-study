import pytest
from fastapi.testclient import TestClient

import defai.api as api
from defai.storage.database import Database


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test.db")

    with Database(db_path) as db:
        db.connection.executemany(
            """
            INSERT INTO transactions
            (signature, success, fee_lamports, account_count, slot, block_time)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                ("older", 1, 5000, 3, 100, 1700000000),
                ("newer", 0, 6000, 4, 200, 1700000100),
            ],
        )
        db.connection.commit()

    monkeypatch.setattr(api, "Database", lambda: Database(db_path))

    with TestClient(api.app) as test_client:
        yield test_client


def test_transaction_history(client):
    response = client.get("/transactions")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert [tx["signature"] for tx in data["transactions"]] == [
        "newer", "older"
    ]
    assert data["transactions"][0]["success"] is False
    assert data["transactions"][1]["success"] is True


def test_transaction_pagination(client):
    response = client.get("/transactions?limit=1&offset=1")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["limit"] == 1
    assert data["offset"] == 1
    assert len(data["transactions"]) == 1
    assert data["transactions"][0]["signature"] == "older"


def test_transaction_page_beyond_end(client):
    response = client.get("/transactions?offset=10")
    assert response.status_code == 200
    assert response.json()["transactions"] == []


@pytest.mark.parametrize(
    "query",
    ["limit=0", "limit=101", "offset=-1", "limit=abc"],
)
def test_invalid_pagination(client, query):
    assert client.get(f"/transactions?{query}").status_code == 422
