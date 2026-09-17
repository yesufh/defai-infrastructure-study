from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

from defai.models import TransactionSummary


class Database:
    """Simple SQLite persistence layer for analyzed Solana transactions."""

    def __init__(self, path: str = "data/defai.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row

        self._create_tables()

    def _create_tables(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                signature TEXT PRIMARY KEY,
                success INTEGER NOT NULL,
                fee_lamports INTEGER NOT NULL,
                account_count INTEGER NOT NULL,
                slot INTEGER,
                block_time INTEGER
            )
            """
        )

        self.connection.commit()

    def save_transactions(
        self,
        transactions: Iterable[TransactionSummary],
    ) -> None:
        """Store transaction summaries without duplicating existing records."""

        self.connection.executemany(
            """
            INSERT OR REPLACE INTO transactions (
                signature,
                success,
                fee_lamports,
                account_count,
                slot,
                block_time
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    tx.signature,
                    int(tx.success),
                    tx.fee_lamports,
                    tx.account_count,
                    tx.slot,
                    tx.block_time,
                )
                for tx in transactions
            ],
        )

        self.connection.commit()

    def count_transactions(self) -> int:
        """Return the number of stored transactions."""

        row = self.connection.execute(
            "SELECT COUNT(*) AS count FROM transactions"
        ).fetchone()

        return int(row["count"])

    def close(self) -> None:
        """Close the database connection."""

        self.connection.close()

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
