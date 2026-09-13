# Data Engineering Code Rules

## 1. Type Enforcement
- Use `Pydantic` for all data models.
- Never use `Any`. Use `TypeVar` or specific `Unions` if necessary.
- Every function in `application/stage/` must have full type hints for inputs and outputs.

## 2. Error Handling
- Use custom exceptions from `shared/exception/`.
- **Fail-Fast**: If a `core_model` record fails validation, quarantine it and raise a `DataQualityError`. Do not proceed with corrupted data.
- Never use bare `except:`. Always catch specific `AdapterError` or `TransformationError`.

## 3. Data Transformations
- Prefer **Polars** or **DuckDB** for transformations to ensure high performance and lazy evaluation.
- Keep transformations **pure**: they take a data frame/dictionary and return a new one. No side effects.
- Side effects (I/O) are restricted to the `infrastructure` layer.

## 4. Performance
- Use `__slots__` for model classes.
- Implement `limit` and `offset` in all `Reader` protocols.
- Avoid Python loops over data; use vectorized operations.
