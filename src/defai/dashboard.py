from __future__ import annotations

from defai.analytics import get_transaction_analytics
from defai.storage.database import Database


def render_dashboard() -> str:
    """Generate a simple HTML dashboard from historical analytics."""

    with Database() as db:
        analytics = get_transaction_analytics(db)
    history = """
        <h2>Recent Transactions</h2>
        <p id="history-status">Loading transactions...</p>
        <div style="overflow-x:auto">
            <table style="width:100%;background:white;text-align:left">
                <thead>
                    <tr>
                        <th>Signature</th>
                        <th>Status</th>
                        <th>Fee (lamports)</th>
                        <th>Slot</th>
                    </tr>
                </thead>
                <tbody id="transaction-rows"></tbody>
            </table>
        </div>
        <script>
        async function loadTransactions() {
            const status = document.getElementById("history-status");
            const body = document.getElementById("transaction-rows");
            try {
                const response = await fetch("/transactions?limit=20");
                if (!response.ok) throw new Error("Request failed");
                const data = await response.json();
                for (const tx of data.transactions) {
                    const row = document.createElement("tr");
                    const values = [
                        tx.signature,
                        tx.success ? "Success" : "Failed",
                        tx.fee_lamports.toLocaleString(),
                        tx.slot ?? "Unknown"
                    ];
                    for (const value of values) {
                        const cell = document.createElement("td");
                        cell.textContent = String(value);
                        cell.style.padding = "12px";
                        row.appendChild(cell);
                    }
                    body.appendChild(row);
                }
                status.textContent = data.total === 0
                    ? "No stored transactions yet."
                    : `Showing ${data.transactions.length} of ${data.total} stored transactions, newest slots first.`;
            } catch (error) {
                status.textContent = "Could not load transactions. Refresh to try again.";
            }
        }
        loadTransactions();
        </script>
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DeFAI Analytics Dashboard</title>
        <style>
        {history}
    {history}
    </body>
            body {{
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 40px auto;
                padding: 0 20px;
                background: #f5f5f5;
            }}

            h1 {{
                margin-bottom: 5px;
            }}

            .subtitle {{
                color: #666;
                margin-bottom: 30px;
            }}

            .metrics {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
            }}

            .card {{
                background: white;
                padding: 24px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            }}

            .value {{
                font-size: 32px;
                font-weight: bold;
            }}

            .label {{
                color: #666;
                margin-top: 8px;
            }}
        </style>
    </head>

    <body>
        <h1>DeFAI Analytics Dashboard</h1>
        <div class="subtitle">Historical Solana transaction analytics</div>

        <div class="metrics">
            <div class="card">
                <div class="value">{analytics.total_transactions}</div>
                <div class="label">Total Transactions</div>
            </div>

            <div class="card">
                <div class="value">{analytics.successful_transactions}</div>
                <div class="label">Successful Transactions</div>
            </div>

            <div class="card">
                <div class="value">{analytics.failed_transactions}</div>
                <div class="label">Failed Transactions</div>
            </div>

            <div class="card">
                <div class="value">{analytics.average_fee_lamports:,.2f}</div>
                <div class="label">Average Fee (Lamports)</div>
            </div>
        </div>
    {history}
    </body>
    </html>
    """
