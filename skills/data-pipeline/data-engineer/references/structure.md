# Data Pipeline Structure

The High-Integrity Data Pipeline follows a strict Hexagonal Medallion pattern.

## Directory Layout

```text
repo/
├── src/
│   ├── application/
│   │   ├── model/          # 💎 Data Contracts
│   │   │   ├── __init__.py
│   │   │   ├── raw_source.py
│   │   │   ├── core_entity.py
│   │   │   └── business_view.py
│   │   ├── port/           # 🔌 Protocols
│   │   │   ├── reader.py   # Protocol for data ingestion
│   │   │   └── writer.py   # Protocol for data persistence
│   │   ├── stage/          # 🏗️ Transformation Logic (Orchestrator-free)
│   │   │   ├── raw.py      # Move data from source to raw storage
│   │   │   ├── core_model.py # Move from raw to silver (cleaning)
│   │   │   └── business_view.py # Move from silver to gold (KPIs)
│   │   └── service/        # Stateless cross-cutting logic
│   ├── infrastructure/
│   │   ├── adapter/        # 🔌 Concrete Implementations
│   │   │   ├── source/     # S3, Kafka, API Readers
│   │   │   └── sink/       # Snowflake, Iceberg, Postgres Writers
│   │   ├── orchestration/  # 🚀 Frameworks (Prefect/Airflow)
│   │   │   ├── flows/
│   │   │   └── dags/
│   │   └── config/         # Environment & Credentials
│   └── shared/
│       ├── exception/      # DataQualityError, SchemaMismatchError
│       └── type_guard/     # Runtime validation helpers
├── tests/
│   ├── unit/               # Testing stages with mocked Readers/Writers
│   ├── integration/        # End-to-end flow with local DuckDB
│   └── property/           # Invariant testing with Hypothesis
├── data/                   # Gitignored local data storage
├── pyproject.toml          # UV configuration
└── justfile                # Task runner
```

## Key Principles

1. **Protocol-Driven**: The `stage` logic only knows about `Protocols` in `application/port/`. It never imports from `infrastructure/adapter/`.
2. **Schema Isolation**: Pydantic models in `application/model/` act as the source of truth for all data movement.
3. **Local-First Development**: Use the `data/` directory and local adapters (DuckDB/Parquet) to develop pipelines without cloud dependencies.
