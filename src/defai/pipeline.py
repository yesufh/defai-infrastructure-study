from .analyzer import analyze_wallet, summarize_transaction
from .models import WalletActivity, TransactionSummary
from .risk import assess_wallet_risk
from .rpc import SolanaRPC
from .storage.database import Database


def analyze_address(
    address: str,
    limit: int = 20,
) -> tuple[WalletActivity, list[TransactionSummary]]:
    """Fetch, persist, analyze, and assess activity for a Solana address."""

    rpc = SolanaRPC()

    signatures = rpc.get_signatures_for_address(
        address,
        limit=limit,
    )

    summaries: list[TransactionSummary] = []

    for item in signatures:
        signature = item["signature"]
        transaction = rpc.get_transaction(signature)

        summaries.append(
            summarize_transaction(signature, transaction)
        )

    # Persist transaction data for future analysis and monitoring.
    with Database() as db:
        db.save_transactions(summaries)

    activity = analyze_wallet(address, summaries)
    assessment = assess_wallet_risk(activity)

    activity.risk_score = assessment.score
    activity.flags = assessment.reasons

    return activity, summaries
