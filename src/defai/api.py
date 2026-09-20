from fastapi import FastAPI

from defai.analytics import get_transaction_analytics
from defai.storage.database import Database


app = FastAPI(
    title="DeFAI Analytics API",
    version="1.0.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "DeFAI Analytics API",
        "status": "running",
    }


@app.get("/analytics")
def analytics() -> dict[str, int | float]:
    with Database() as db:
        summary = get_transaction_analytics(db)

    return {
        "total_transactions": summary.total_transactions,
        "successful_transactions": summary.successful_transactions,
        "failed_transactions": summary.failed_transactions,
        "total_fees_lamports": summary.total_fees_lamports,
        "average_fee_lamports": summary.average_fee_lamports,
    }
