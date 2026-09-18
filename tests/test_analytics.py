from defai.analytics import get_transaction_analytics
from defai.models import TransactionSummary
from defai.storage.database import Database


def test_transaction_analytics(tmp_path):
    db = Database(str(tmp_path / "test.db"))

    transactions = [
        TransactionSummary(
            signature="tx1",
            slot=1,
            block_time=1000,
            success=True,
            fee_lamports=5000,
            account_count=4,
            log_count=2,
        ),
        TransactionSummary(
            signature="tx2",
            slot=2,
            block_time=2000,
            success=False,
            fee_lamports=10000,
            account_count=6,
            log_count=3,
        ),
    ]

    db.save_transactions(transactions)

    analytics = get_transaction_analytics(db)

    assert analytics.total_transactions == 2
    assert analytics.successful_transactions == 1
    assert analytics.failed_transactions == 1
    assert analytics.total_fees_lamports == 15000
    assert analytics.average_fee_lamports == 7500.0

    db.close()

