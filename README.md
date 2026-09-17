# DeFAI Systems Lab

### On-Chain Intelligence & Risk Monitoring

A read-only Solana blockchain intelligence prototype that retrieves public transaction data, extracts activity metrics, and applies a transparent deterministic risk model.

## Why I Built It

This project grew out of my experience researching the Solana and DeFAI ecosystem. I became interested in treating fast-moving blockchain research as an infrastructure problem: collect observable events, turn them into structured data, apply explicit rules, and make the system reproducible.

The current version deliberately focuses on public, read-only data. It does not execute trades, custody assets, or request private keys.

## Architecture

```text
Solana JSON-RPC
      |
      v
RPC Client
      |
      v
Transaction Parser
      |
      v
Wallet Activity Metrics
      |
      v
Deterministic Risk Engine
      |
      v
CLI Report
```

## Features

- Read-only Solana JSON-RPC client
- Recent transaction retrieval for a public address
- Transaction success/failure analysis
- Fee and account-count metrics
- Transparent risk scoring rules
- Command-line interface
- Unit tests with Pytest
- GitHub Actions CI
- Docker support
- No private keys or transaction signing

## Tech Stack

- Python 3.12
- Solana JSON-RPC
- HTTPX
- Pydantic-compatible environment
- Pytest
- Rich
- Docker
- GitHub Actions

## Setup

```bash
git clone git@github.com:yesufh/defai-infrastructure-study.git
cd defai-infrastructure-study

python -m venv .venv
source .venv/bin/activate

# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt
```

Optional configuration:

```bash
cp .env.example .env
```

## Run Tests

```bash
PYTHONPATH=src pytest -v
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
pytest -v
```

## Analyze a Public Solana Address

```bash
PYTHONPATH=src python -m defai.cli YOUR_SOLANA_ADDRESS --limit 20
```

Example:

```bash
PYTHONPATH=src python -m defai.cli 11111111111111111111111111111111 --limit 5
```

The CLI reports:

- transactions analyzed
- successful transactions
- failed transactions
- success rate
- total fees
- deterministic risk score
- risk flags

## Risk Model

The initial model is intentionally simple and explainable.

| Signal | Condition | Score |
|---|---|---:|
| Failure rate | >= 30% | +40 |
| Failure rate | >= 10% | +20 |
| Average fee | > 10,000 lamports | +20 |
| Small sample | < 5 transactions | +10 |

Scores are capped at 100.

- 0–39: LOW
- 40–69: MEDIUM
- 70–100: HIGH

This is an engineering prototype, **not a financial risk rating or investment recommendation**.

## Repository Structure

```text
src/defai/
├── analyzer.py    # Transaction and wallet analysis
├── cli.py         # Command-line interface
├── config.py      # Environment configuration
├── models.py      # Domain models
├── pipeline.py    # End-to-end orchestration
├── risk.py        # Deterministic risk engine
└── rpc.py         # Solana JSON-RPC client

tests/
├── test_analyzer.py
└── test_risk.py

docs/
├── architecture.md
└── methodology.md
```

## Safety

The application is read-only. Never commit:

- private keys
- seed phrases
- API secrets
- `.env` files containing credentials

## Roadmap

- [x] RPC ingestion
- [x] Transaction analysis
- [x] Risk engine
- [x] CLI
- [x] Unit tests
- [x] GitHub Actions CI
- [x] Docker
- [ ] Async/WebSocket ingestion
- [ ] SQLite/PostgreSQL event storage
- [ ] Prometheus metrics
- [ ] Grafana dashboard
- [ ] Rust performance component
- [ ] Agentic explanation layer

## Author

**Yesuf Hassen**

IT Infrastructure · Systems Engineering · DeFAI Research
