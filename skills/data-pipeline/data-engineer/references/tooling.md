# Tooling & Ecosystem

## 1. Environment & Package Management
- **uv**: Primary package manager and task runner.
- **prek**: Pre-commit hook management.

## 2. Processing Engines
- **Polars**: Fast, memory-efficient data frames for Python.
- **DuckDB**: In-process SQL OLAP database for local development and fast aggregations.

## 3. Orchestration
- **Prefect**: Preferred for functional, dynamic workflows.
- **Airflow**: Use for static, complex DAG dependencies if required by infrastructure.

## 4. Validation & Quality
- **Pydantic**: Runtime data validation and settings management.
- **Great Expectations**: (Optional) For complex dataset-level profiling and validation.
- **Hypothesis**: Property-based testing for edge-case detection.

## 5. Storage Formats
- **Parquet**: Default columnar format for Bronze/Silver.
- **Iceberg/Delta**: For ACID transactions on object storage if scaling beyond local files.
