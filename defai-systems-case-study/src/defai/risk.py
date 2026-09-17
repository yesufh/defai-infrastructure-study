from .models import RiskAssessment, WalletActivity


def assess_wallet_risk(activity: WalletActivity) -> RiskAssessment:
    if activity.transactions_analyzed == 0:
        return RiskAssessment(
            score=0,
            level="UNKNOWN",
            reasons=["No transaction history available."],
        )

    score = 0.0
    reasons: list[str] = []

    failure_rate = (
        activity.failed_transactions
        / activity.transactions_analyzed
    )

    if failure_rate >= 0.30:
        score += 40
        reasons.append("High transaction failure rate.")
    elif failure_rate >= 0.10:
        score += 20
        reasons.append("Elevated transaction failure rate.")

    if activity.average_fee_lamports > 10_000:
        score += 20
        reasons.append("Elevated average transaction fee.")

    if activity.transactions_analyzed < 5:
        score += 10
        reasons.append("Small observation window.")

    score = min(score, 100)

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return RiskAssessment(
        score=score,
        level=level,
        reasons=reasons,
    )
