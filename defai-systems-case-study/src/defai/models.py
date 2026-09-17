from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TransactionSummary:
    signature: str
    slot: Optional[int]
    success: bool
    fee_lamports: int
    account_count: int
    log_count: int

    @property
    def fee_sol(self) -> float:
        return self.fee_lamports / 1_000_000_000


@dataclass
class WalletActivity:
    address: str
    transactions_analyzed: int
    successful_transactions: int
    failed_transactions: int
    total_fees_lamports: int
    average_fee_lamports: float
    success_rate: float
    risk_score: float
    flags: list[str] = field(default_factory=list)

    @property
    def total_fees_sol(self) -> float:
        return self.total_fees_lamports / 1_000_000_000


@dataclass
class RiskAssessment:
    score: float
    level: str
    reasons: list[str]
