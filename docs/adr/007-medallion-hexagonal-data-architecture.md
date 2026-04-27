# ADR 007: Adoption of Medallion Hexagonal Architecture for Data Pipelines

**Date:** 2026-04-27
**Status:** Accepted

## Context
Standard data engineering practices often lead to "spaghetti" pipelines where business logic, data cleaning, and orchestration (e.g., Prefect/Airflow tasks) are tightly coupled. This results in:
1. **Low Testability**: Pipelines can only be tested with a running database or orchestrator.
2. **Vendor Lock-in**: Hard-coding orchestrator decorators inside transformation logic makes switching frameworks difficult.
3. **Data Quality Issues**: Lack of explicit schema enforcement between ingestion and business-ready layers.

We need a structure that brings the high-integrity standards of our `python-app` family (Hexagonal Architecture) to the data domain while respecting the natural stages of data refinement.

## Decision
We will adopt the **Medallion Hexagonal Architecture** for the `data-pipeline/data-engineer` skill. This architecture combines the Port/Adapter pattern with standardized Medallion layers:

1. **Hexagonal Decoupling**:
    - **Ports (`application/port`)**: Protocols for data reading and writing.
    - **Adapters (`infrastructure/adapter`)**: Implementation for S3, DuckDB, Snowflake, etc.
    - **Orchestration (`infrastructure/orchestration`)**: Framework-specific drivers (Prefect Flows/Airflow DAGs).
2. **Medallion Logic (`application/stage`)**:
    - **`raw`**: Ingestion of immutable source data.
    - **`core_model`**: Single Source of Truth (SSOT) with strict typing via Pydantic.
    - **`business_view`**: Highly optimized datasets for consumer use cases.
3. **Modern Data Stack Tooling**:
    - **Polars/DuckDB**: Standardized as the primary compute engines for their lazy evaluation and high performance.
    - **Pydantic**: Mandatory for schema validation at every layer boundary.
    - **uv**: Standardized for dependency and workspace management.

## Consequences
- **Positive**:
    - **Framework Independence**: Transformation logic can be run and tested without Prefect or Airflow.
    - **Testable Data Logic**: Stages can be unit-tested using mocked data frames (Polars/Pandas) in milliseconds.
    - **High Integrity**: Pydantic models ensure that malformed data is caught and quarantined before reaching business views.
    - **Local-First Development**: Developers can run full pipelines using local adapters (DuckDB/Parquet) without cloud connectivity.
- **Negative**:
    - **Setup Overhead**: Requires more boilerplate (Protocols/Adapters) compared to a single-file script.
    - **Learning Curve**: Requires understanding of both Hexagonal principles and the Medallion model.

## Alternatives Considered
- **Direct Orchestrator Scripts**: Writing transformations directly inside Airflow operators or Prefect tasks. Rejected due to poor testability and tight coupling.
- **DBT-Only Approach**: Using SQL (DBT) for all transformations. Rejected because it limits the ability to integrate complex Python-based logic, ML models, and high-integrity safety rules (Power of 10).
- **Generic Python App Structure**: Using the standard `python-app/developer` structure. Rejected as it lacks explicit support for the staged data refinement process (Medallion) essential for data engineering.
