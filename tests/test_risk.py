from defai.models import WalletActivity
from defai.risk import assess_wallet_risk


def test_low_risk_wallet():
    activity = WalletActivity(
        address="test",
        transactions_analyzed=20,
        successful_transactions=20,
        failed_transactions=0,
        total_fees_lamports=20_000,
        average_fee_lamports=1_000,
        success_rate=1.0,
        risk_score=0,
    )

    result = assess_wallet_risk(activity)

    assert result.level == "LOW"
    assert result.score < 40


def test_high_failure_rate():
    activity = WalletActivity(
        address="test",
        transactions_analyzed=20,
        successful_transactions=10,
        failed_transactions=10,
        total_fees_lamports=20_000,
        average_fee_lamports=1_000,
        success_rate=0.5,
        risk_score=0,
    )

    result = assess_wallet_risk(activity)

    assert result.score >= 40


def test_empty_history():
    activity = WalletActivity(
        address="test",
        transactions_analyzed=0,
        successful_transactions=0,
        failed_transactions=0,
        total_fees_lamports=0,
        average_fee_lamports=0,
        success_rate=0,
        risk_score=0,
    )

    result = assess_wallet_risk(activity)

    assert result.level == "UNKNOWN"
