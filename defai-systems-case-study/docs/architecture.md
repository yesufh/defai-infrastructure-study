# Architecture

## Overview

DeFAI Systems Lab is a read-only blockchain intelligence pipeline.

```text
                 +----------------------+
                 |     Solana RPC       |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |      RPC Client      |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Transaction Parser   |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Activity Analyzer    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Deterministic Risk   |
                 | Engine               |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | CLI / Reporting      |
                 +----------------------+
```

## Components

### RPC Client

`src/defai/rpc.py` provides a small read-only interface over Solana JSON-RPC.

### Analyzer

`src/defai/analyzer.py` transforms raw transaction responses into stable domain models.

### Risk Engine

`src/defai/risk.py` applies transparent rules to the activity model.

### Pipeline

`src/defai/pipeline.py` orchestrates ingestion, parsing, analysis, and scoring.

### CLI

`src/defai/cli.py` provides a human-readable terminal interface.

## Design Principles

- Read-only by default
- No private-key handling
- Explicit and testable rules
- Small modular components
- Reproducible local execution
- Automated testing through CI
