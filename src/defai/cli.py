import argparse

from rich.console import Console
from rich.table import Table

from .pipeline import analyze_address

console = Console()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="DeFAI Systems Lab - Solana on-chain intelligence CLI"
    )
    parser.add_argument(
        "address",
        help="Solana wallet/public address",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of recent transactions to analyze (1-1000)",
    )

    args = parser.parse_args()

    console.print("\n[bold]DeFAI Systems Lab[/bold]")
    console.print("Read-only Solana wallet analysis\n")

    try:
        activity, transactions = analyze_address(
            args.address,
            args.limit,
        )
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise SystemExit(1) from exc

    table = Table(title="Wallet Activity")
    table.add_column("Metric")
    table.add_column("Value")

    table.add_row("Address", activity.address)
    table.add_row("Transactions", str(activity.transactions_analyzed))
    table.add_row("Successful", str(activity.successful_transactions))
    table.add_row("Failed", str(activity.failed_transactions))
    table.add_row("Success Rate", f"{activity.success_rate:.1%}")
    table.add_row("Fees", f"{activity.total_fees_sol:.6f} SOL")
    table.add_row(
        "Risk Score",
        f"{activity.risk_score:.1f}/100",
    )

    console.print(table)

    if activity.flags:
        console.print("\n[bold]Risk Flags[/bold]")
        for flag in activity.flags:
            console.print(f"  • {flag}")

    console.print(f"\nAnalyzed {len(transactions)} transactions.")


if __name__ == "__main__":
    main()
