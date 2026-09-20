from __future__ import annotations

from defai.analytics import get_transaction_analytics
from defai.storage.database import Database


def generate_metrics() -> str:
    """Generate Prometheus-compatible metrics from stored transactions."""

    with Database() as db:
        analytics = get_transaction_analytics(db)

    metrics = [
        "# HELP defai_transactions_total Total number of stored transactions.",
        "# TYPE defai_transactions_total gauge",
        f"defai_transactions_total {analytics.total_transactions}",
        "",
        "# HELP defai_transactions_successful Number of successful transactions.",
        "# TYPE defai_transactions_successful gauge",
        f"defai_transactions_successful {analytics.successful_transactions}",
        "",
        "# HELP defai_transactions_failed Number of failed transactions.",
        "# TYPE defai_transactions_failed gauge",
        f"defai_transactions_failed {analytics.failed_transactions}",
        "",
        "# HELP defai_average_fee_lamports Average transaction fee in lamports.",
        "# TYPE defai_average_fee_lamports gauge",
        f"defai_average_fee_lamports {analytics.average_fee_lamports}",
    ]

    return "\n".join(metrics) + "\n"
