---
name: data-engineer
description: Source of truth for high-integrity Data Engineering, focusing on Medallion Hexagonal architecture, idempotency, and strict data contracts.
---

## 1. Architectural Integrity

### Hexagonal Medallion Structure

Pipelines must be organized into three distinct Medallion layers within a Hexagonal framework to ensure separation of concerns, testability, and framework independence:

- **`raw` (Bronze)**: Immutable ingestion of source data. No transformations. Responsible for checkpointing and capture of technical metadata.
- **`core_model` (Silver)**: The "Single Source of Truth." Responsible for type enforcement (via Pydantic), cleaning, normalization, and deduplication. No business logic.
- **`business_view` (Gold)**: Consumer-facing datasets. Responsible for aggregations, business KPIs, and feature engineering. Highly optimized for specific use cases.

### Design Principles

- **Idempotency**: Every task must be repeatable without side effects. Running a transformation multiple times must yield the identical state.
- **Orchestration Decoupling**: Business logic (Stages) must be independent of the orchestrator (Prefect/Airflow). The orchestrator is a "driver" in the `infrastructure` layer.
- **Late Materialization**: Prefer transformations on lazy data frames (Polars/DuckDB) until the final write to a sink.
- **Fail-Closed Pipelines**: If data quality checks (TypeGuards/Great Expectations) fail at a layer boundary, the pipeline must abort before downstream propagation.

## 2. Control & Safety (The Data Power of 10)

1. **Immutable Sources**: Raw data is never modified or deleted after ingestion.
2. **Schema-First**: Every transition between layers must be validated by a Pydantic model.
3. **Hard Compute Bounds**: Every data read must implement `LIMIT` or `CHUNK_SIZE` to prevent memory exhaustion.
4. **Deterministic Time**: Use event-time processing over processing-time. Always include `ingested_at` and `source_timestamp` metadata.
5. **No Blind Retries**: Retries must be exponential and capped. Tasks must be atomic to ensure a retry doesn't create duplicate records.
6. **Pure Transformations**: Logic in `core_model` and `business_view` must be I/O-free and deterministic.
7. **Explicit State**: Use checkpointing or high-water marks to ensure resumeability after failure.
8. **Dependency Injection**: Data Readers and Writers (Adapters) must be passed to stages, never instantiated internally.
9. **No Magic Schemas**: Forbidden: dynamic schema inference in production. All schemas must be explicitly declared.
10. **Validation at Boundary**: Use `TypeGuard` at the entry point of every stage.

## 3. Testing & Verification

- **Unit Testing**: Test `core_model` and `business_view` transformations using static mocked data frames.
- **Property-Based Testing**: Use `Hypothesis` to ensure schemas handle edge cases (nulls, empty strings, overflow) without crashing.
- **Integration Testing**: Verify end-to-end flow from `raw` to `business_view` using local `DuckDB` or TestContainers.

## 4. Operational Workflow

### Project Template

```text
repo/
├── src/
│   ├── application/
│   │   ├── model/          # Pydantic Schemas (__slots__ used)
│   │   ├── port/           # Protocols for Readers/Writers
│   │   └── stage/          # Pure logic (raw, core_model, business_view)
│   ├── infrastructure/
│   │   ├── adapter/        # S3, Snowflake, Kafka implementations
│   │   ├── orchestration/  # Prefect Flows or Airflow DAGs
│   │   └── config/         # Constants and Catalog settings
│   └── shared/
│       ├── exception/      # Pipeline-specific failures
│       └── type_guard/     # Runtime quality validators
├── tests/
│   ├── unit/               # Mocked transformation tests
│   ├── integration/        # End-to-end pipeline tests
│   └── property/           # Hypothesis tests
└── data/                   # Local dev/test data (gitignored)
```

## Project Interaction

- **Trigger**: "Implement the `core_model` stage for [source]"
- **Trigger**: "Define the Pydantic schemas for [business_view]"
- **Trigger**: "Refactor this pipeline to be idempotent"
- **Trigger**: "Create a Prefect deployment for the [name] flow"
- **Trigger**: "Add property-based tests for the [transformation] logic"
