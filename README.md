# DeFAI Systems Lab

### On-Chain Intelligence & Risk Monitoring Platform

DeFAI Systems Lab is a read-only Solana analytics platform that ingests public blockchain transaction data, transforms it into structured records, persists historical data in SQLite, calculates wallet activity metrics, applies deterministic risk rules, and exposes results through a REST API, web dashboard, and Prometheus-compatible monitoring endpoint.

The project demonstrates an end-to-end backend and data pipeline built around real public blockchain data.

## Why I Built It

This project grew out of my experience researching the Solana and DeFAI ecosystem. I found myself repeatedly collecting and analyzing on-chain activity manually and became interested in treating that workflow as an infrastructure problem:

**collect events → structure data → persist records → analyze history → expose results → monitor the system**

The platform is intentionally read-only. It does not execute trades, custody assets, sign transactions, or request private keys.

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
SQLite Persistence
       |
       v
Historical Analytics
       |
       +------------------+
       |                  |
       v                  v
Risk Engine          FastAPI REST API
                          |
                +---------+---------+
                |                   |
                v                   v
          Web Dashboard       /metrics Endpoint
                              (Prometheus format)
```

## Features

- Read-only Solana JSON-RPC integration
- Public wallet transaction retrieval
- Transaction parsing and normalization
- SQLite persistence for historical transaction records
- Duplicate-safe transaction storage
- SQL-based historical analytics
- Transaction success/failure metrics
- Fee and account activity analysis
- Explainable deterministic risk scoring
- FastAPI REST API
- Browser-based analytics dashboard
- Prometheus-compatible monitoring metrics
- Command-line interface
- Automated tests with Pytest
- GitHub Actions continuous integration
- Docker support
- No private keys or transaction signing

## Tech Stack

- Python 3.12
- SQL / SQLite
- FastAPI
- Uvicorn
- Solana JSON-RPC
- HTTPX
- Pytest
- Rich
- Docker
- GitHub Actions

## Setup

Clone the repository:

```bash
git clone git@github.com:yesufh/defai-infrastructure-study.git
cd defai-infrastructure-study
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Optional configuration:

```bash
cp .env.example .env
```

## Run Tests

```bash
PYTHONPATH=src python3 -m pytest
```

## Analyze a Public Solana Address

```bash
PYTHONPATH=src python3 -m defai.cli YOUR_SOLANA_ADDRESS --limit 20
```

Example:

```bash
PYTHONPATH=src python3 -m defai.cli Vote111111111111111111111111111111111111111 --limit 5
```

The pipeline retrieves public transaction data, analyzes the transactions, stores structured records in SQLite, and calculates wallet activity and risk indicators.

## Run the API

Start the FastAPI server:

```bash
PYTHONPATH=src python3 -m uvicorn defai.api:app --reload
```

The application runs locally at:

```text
http://127.0.0.1:8000
```

### API Endpoints

| Endpoint | Description |
|---|---|
| `/` | API health/status |
| `/analytics` | Historical transaction analytics as JSON |
| `/dashboard` | Browser-based analytics dashboard |
| `/metrics` | Prometheus-compatible monitoring metrics |
| `/docs` | Interactive FastAPI/OpenAPI documentation |

Example analytics response:

```json
{
  "total_transactions": 5,
  "successful_transactions": 5,
  "failed_transactions": 0,
  "total_fees_lamports": 25000,
  "average_fee_lamports": 5000.0
}
```

## Analytics

Historical analytics are calculated from persisted SQLite transaction records.

Current metrics include:

- total stored transactions
- successful transactions
- failed transactions
- total transaction fees
- average transaction fee

Persisting transactions allows analysis to operate on historical data rather than only the latest RPC response.

## Monitoring

The `/metrics` endpoint exposes application analytics in a Prometheus-compatible text format.

Example:

```text
# HELP defai_transactions_total Total number of stored transactions.
# TYPE defai_transactions_total gauge
defai_transactions_total 5

# HELP defai_transactions_successful Number of successful transactions.
# TYPE defai_transactions_successful gauge
defai_transactions_successful 5

# HELP defai_transactions_failed Number of failed transactions.
# TYPE defai_transactions_failed gauge
defai_transactions_failed 0
```

This provides a foundation for integration with monitoring systems such as Prometheus and Grafana.

## Risk Model

The current risk model is intentionally deterministic and explainable.

| Signal | Condition | Score |
|---|---|---:|
| Failure rate | >= 30% | +40 |
| Failure rate | >= 10% | +20 |
| Average fee | > 10,000 lamports | +20 |
| Small sample | < 5 transactions | +10 |

Scores are capped at 100.

- **0–39:** LOW
- **40–69:** MEDIUM
- **70–100:** HIGH

The model is an engineering prototype designed to demonstrate transparent rule-based analysis. It is **not a financial risk rating or investment recommendation**.

## Repository Structure

```text
src/defai/
├── analytics.py        # Historical SQL analytics
├── analyzer.py         # Transaction and wallet analysis
├── api.py              # FastAPI REST endpoints
├── cli.py              # Command-line interface
├── config.py           # Environment configuration
├── dashboard.py        # Browser analytics dashboard
├── metrics.py          # Prometheus-compatible metrics
├── models.py           # Domain models
├── pipeline.py         # End-to-end orchestration
├── risk.py             # Deterministic risk engine
├── rpc.py              # Solana JSON-RPC client
└── storage/
    ├── __init__.py
    └── database.py     # SQLite persistence layer

tests/
├── test_analytics.py
├── test_analyzer.py
├── test_api.py
└── test_risk.py

docs/
├── architecture.md
└── methodology.md
```

## Engineering Focus

This project focuses on several areas of software and data engineering:

- API integration and external data ingestion
- data transformation and domain modeling
- relational persistence with SQL
- historical analytics
- modular backend architecture
- REST API development
- observability and monitoring
- automated testing
- containerization
- continuous integration

## Safety

The application operates only on public blockchain data.

Never commit:

- private keys
- seed phrases
- API secrets
- `.env` files containing credentials

The application does not sign or submit blockchain transactions.

## Roadmap

### Completed

- [x] Solana JSON-RPC ingestion
- [x] Transaction parsing and analysis
- [x] Deterministic risk engine
- [x] Command-line interface
- [x] SQLite transaction persistence
- [x] Historical SQL analytics
- [x] FastAPI REST API
- [x] Web analytics dashboard
- [x] Prometheus-compatible metrics endpoint
- [x] Automated Pytest suite
- [x] GitHub Actions CI
- [x] Docker support

### Potential Extensions

- [ ] Async or WebSocket-based ingestion
- [ ] PostgreSQL support
- [ ] Grafana visualization
- [ ] Expanded wallet-level historical analytics
- [ ] Agent-assisted explanations of analytics
- [ ] Rust performance component

## Disclaimer

This repository is an engineering and research project. It does not provide financial advice, investment recommendations, or automated trading functionality.

## Author

**Yesuf Hassen**

Information Systems · Software & Data Engineering · Infrastructure
