from __future__ import annotations

from dataclasses import dataclass

from defai.storage.database import Database


@dataclass
class TransactionAnalytics:
    total_transactions: int
    successful_transactions: int
    failed_transactions: int
    total_fees_lamports: int
    average_fee_lamports: float


def get_transaction_analytics(
    db: Database,
) -> TransactionAnalytics:
    """Calculate historical analytics from stored transactions."""

    row = db.connection.execute(
        """
        SELECT
            COUNT(*) AS total_transactions,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END)
                AS successful_transactions,
            SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END)
                AS failed_transactions,
            COALESCE(SUM(fee_lamports), 0) AS total_fees_lamports,
            COALESCE(AVG(fee_lamports), 0) AS average_fee_lamports
        FROM transactions
        """
    ).fetchone()

    return TransactionAnalytics(
        total_transactions=int(row["total_transactions"]),
        successful_transactions=int(row["successful_transactions"] or 0),
        failed_transactions=int(row["failed_transactions"] or 0),
        total_fees_lamports=int(row["total_fees_lamports"]),
        average_fee_lamports=float(row["average_fee_lamports"]),
    )
