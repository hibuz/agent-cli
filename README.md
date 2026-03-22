# Agent-Based Commerce Platform Automation

This project aims to build an end-to-end automation platform for onboarding, testing, deploying, and monitoring shopping agents (fashion stylist, beauty consultant, purchase-execution, etc.) while integrating with existing LotteON systems.

## Overview

The platform consists of:
- **Agent SDK Wrapper**: LangChain-based agent base class and registration API.
- **Marketplace Portal**: UI for browsing and searching agents.
- **Orchestration Engine**: Temporal workflows for agent chaining.
- **Data Pipeline**: Kafka, Flink/Spark, Feast feature store, and Redis.
- **Monitoring & CI/CD**: OpenTelemetry, Jaeger, Prometheus, Grafana, and GitHub Actions.
- **Beta Launch & Iteration**: Internal testing and feedback.

## Getting Started

See [PLAN.md](PLAN.md) for the 12-week implementation plan and [PROGRESS.md](PROGRESS.md) for current progress.

## License

MIT