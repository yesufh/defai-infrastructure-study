# Architecture

## Overview

DeFAI Systems Lab is a read-only Solana data and analytics platform that collects public blockchain transaction data, converts it into structured records, persists historical data, performs analytics and deterministic risk analysis, and exposes results through API, dashboard, and monitoring interfaces.

## System Flow

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
       +-------------------+
       |                   |
       v                   v
Activity Analyzer      FastAPI REST API
       |                   |
       v             +-----+------+
Deterministic         |            |
Risk Engine           v            v
       |          Dashboard     /metrics
       v                       Monitoring
CLI Reporting
