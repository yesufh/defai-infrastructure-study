from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

from defai.analytics import get_transaction_analytics
from defai.dashboard import render_dashboard
from defai.metrics import generate_metrics
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


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> str:
    return render_dashboard()


@app.get("/metrics", response_class=PlainTextResponse)
def metrics() -> str:
    return generate_metrics()


@app.get("/transactions")
def transactions(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict:
    with Database() as db:
        total = db.count_transactions()
        rows = db.connection.execute(
            """
            SELECT signature, success, fee_lamports,
                   account_count, slot, block_time
            FROM transactions
            ORDER BY slot DESC, signature ASC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "transactions": [
            {**dict(row), "success": bool(row["success"])}
            for row in rows
        ],
    }
