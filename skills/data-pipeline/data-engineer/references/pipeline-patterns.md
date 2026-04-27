# Pipeline Patterns

## 1. Idempotency Pattern
Every write operation must be idempotent.
- **Append-only**: Include a `run_id` and `inserted_at` timestamp.
- **Overwrite**: Use atomic "Swap" operations or partition-level overwrites.
- **Upsert**: Use a natural business key and a `updated_at` timestamp for deduplication.

## 2. Medallion Flow
- **Raw**: Capture source as-is. Add technical metadata (`source_file`, `ingested_at`).
- **Core Model**: Clean strings, cast types, handle nulls, and enforce the schema. This layer should be optimized for joins.
- **Business View**: Aggregate data for BI tools. Use wide tables or specific stars-schemas.

## 3. Checkpointing
- Use a `High Watermark` pattern: Store the last processed `source_timestamp` in a state store (e.g., DuckDB, Redis, or Prefect Variable).
- The `Reader` protocol must accept a `since: datetime` parameter.

## 4. Quarantine Pattern
- Records that fail `core_model` validation are written to a `quarantine` table/folder instead of being dropped.
- This allows for manual inspection and reprocessing without breaking the pipeline.
