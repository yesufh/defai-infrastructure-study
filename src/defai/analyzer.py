from typing import Any

from .models import TransactionSummary, WalletActivity


def summarize_transaction(
    signature: str,
    transaction: dict[str, Any] | None,
) -> TransactionSummary:
    if transaction is None:
        return TransactionSummary(
            signature=signature,
            slot=None,
            success=False,
            fee_lamports=0,
            account_count=0,
            log_count=0,
        )

    meta = transaction.get("meta") or {}
    message = transaction.get("transaction", {}).get("message", {})

    account_keys = message.get("accountKeys", [])
    logs = meta.get("logMessages") or []

    return TransactionSummary(
        signature=signature,
        slot=transaction.get("slot"),
        success=meta.get("err") is None,
        fee_lamports=meta.get("fee", 0),
        account_count=len(account_keys),
        log_count=len(logs),
    )


def analyze_wallet(
    address: str,
    transactions: list[TransactionSummary],
) -> WalletActivity:
    total = len(transactions)

    if total == 0:
        return WalletActivity(
            address=address,
            transactions_analyzed=0,
            successful_transactions=0,
            failed_transactions=0,
            total_fees_lamports=0,
            average_fee_lamports=0,
            success_rate=0,
            risk_score=0,
        )

    successful = sum(tx.success for tx in transactions)
    failed = total - successful
    total_fees = sum(tx.fee_lamports for tx in transactions)
    average_fee = total_fees / total

    return WalletActivity(
        address=address,
        transactions_analyzed=total,
        successful_transactions=successful,
        failed_transactions=failed,
        total_fees_lamports=total_fees,
        average_fee_lamports=average_fee,
        success_rate=successful / total,
        risk_score=0,
    )
