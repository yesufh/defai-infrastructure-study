from defai.analyzer import summarize_transaction


def test_successful_transaction():
    transaction = {
        "slot": 123,
        "transaction": {
            "message": {
                "accountKeys": [{}, {}],
            }
        },
        "meta": {
            "err": None,
            "fee": 5000,
            "logMessages": ["Program executed"],
        },
    }

    result = summarize_transaction("abc", transaction)

    assert result.signature == "abc"
    assert result.slot == 123
    assert result.success is True
    assert result.fee_lamports == 5000
    assert result.account_count == 2


def test_failed_transaction():
    transaction = {
        "slot": 456,
        "transaction": {
            "message": {
                "accountKeys": [],
            }
        },
        "meta": {
            "err": {"error": "failed"},
            "fee": 5000,
            "logMessages": [],
        },
    }

    result = summarize_transaction("xyz", transaction)

    assert result.success is False
