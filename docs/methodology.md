# Methodology

## Motivation

The project started from personal research into the Solana and DeFAI ecosystem and the observation that fast-moving blockchain environments create information and operational problems that can be treated as systems-engineering problems.

The prototype therefore follows a simple pipeline:

```text
Observe -> Normalize -> Analyze -> Score -> Report
```

## Current Signals

The initial implementation uses public transaction metadata:

- transaction success/failure
- transaction fees
- number of accounts referenced
- recent observation-window size

## Risk Model

The model is deliberately deterministic.

Higher failure rates increase the score. Elevated average fees add a signal. Small samples receive an uncertainty flag.

The score is intended to demonstrate explainable system rules, not to predict market behavior.

## Limitations

The current implementation:

- analyzes only a recent transaction window
- does not model token prices
- does not identify all protocol interactions
- does not perform predictive modeling
- does not execute transactions
- should not be interpreted as financial advice

## Future Research

Potential extensions:

1. asynchronous ingestion
2. WebSocket event streaming
3. persistent event storage
4. protocol/program classification
5. anomaly detection
6. Prometheus metrics
7. dashboarding
8. Rust performance benchmarks
9. agent-generated explanations with human approval gates
