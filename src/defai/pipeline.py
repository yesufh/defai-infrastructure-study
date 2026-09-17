from .analyzer import analyze_wallet, summarize_transaction
from .models import WalletActivity, TransactionSummary
from .risk import assess_wallet_risk
from .rpc import SolanaRPC


def analyze_address(
    address: str,
    limit: int = 20,
) -> tuple[WalletActivity, list[TransactionSummary]]:
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

    activity = analyze_wallet(address, summaries)
    assessment = assess_wallet_risk(activity)

    activity.risk_score = assessment.score
    activity.flags = assessment.reasons

    return activity, summaries
