# Monorepo Project Structure

Prefer a monorepo structure using `uv` workspaces for complex projects with multiple specialized packages.

```text
/
├── pyproject.toml       # Workspace-level config (e.g., [tool.uv.workspace])
├── justfile             # Root tasks (e.g., just run-all, just test-all)
├── TODO.md              # Monorepo-level backlog
├── assets/              # Centralized assets shared across packages
│   ├── fonts/
│   ├── images/
│   └── tilemaps/
├── Environment/         # Specialized simulation package
│   ├── pyproject.toml
│   ├── justfile
│   ├── TODO.md          # Project backlog
│   └── src/permanence_env/
├── Agents/              # Specialized agent package
│   ├── pyproject.toml
│   ├── justfile
│   ├── TODO.md          # Project backlog
│   └── src/permanence_agents/
└── .venv/               # Single shared virtual environment
```

# Templates

## Application

```
myapp-repo/
├── application/
│   ├── model/
│   ├── port/
│   ├── service/         # 👈 See concerns / suggestions
│   └── use_case/
├── infrastructure/
│   ├── adapter/
│   └── config/           # 👈 Configuration loading
│       ├── __init__.py
│       └── settings.py
├── presentation/
│   ├── api/
│   ├── cli/
│   └── web/
└── shared/
	├── constant/         # 👈 App-wide constants
	│   ├── __init__.py
	│   ├── limit.py
	│   └── default.py
	├── exception/
	└── typing/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── property/         # 👈 Property-based tests (Hypothesis)
├── benchmarks/           # 👈 Performance regression tests
├── docs/
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

### Concerns & Suggestions

#### 1. `service/` vs `use_case/` — Overlap Risk

These often blur together. My suggestion:

| Package     | Purpose                                                               | Example                                         |
| ----------- | --------------------------------------------------------------------- | ----------------------------------------------- |
| `use_case/` | **Single action**, application-level orchestration                    | `CreateOrderUseCase`, `AuthenticateUserUseCase` |
| `service/`  | **Domain services**, stateless business logic shared across use cases | `PricingService`, `TaxCalculationService`       |

**Alternative:** Drop `service/`, put domain services in `model/service.py` if they're truly domain-centric. Keeps `application/` focused on orchestration.

---

#### 2. Mirrors `port/` — makes the Port/Adapter pattern explicit:

```
application/port/repository.py    → Protocol
infrastructure/adapter/postgres_repository.py → Implementation
```

---

#### 3. Consider `shared/` or `common/`

For cross-cutting concerns:

```
├── shared/
│   ├── exception/    # Custom exceptions
│   ├── typing/       # TypeGuards, custom types
│   └── constant/     # App-wide constants (MAX_ITERATIONS, etc.)
```

---

## Pipeline

```
mypipeline-repo/
├── application/
│   ├── model/            # Domain models, data schemas
│   ├── port/             # Protocols for sources, sinks, transformers
│   ├── step/             # 👈 Individual pipeline steps
│   │   ├── __init__.py
│   │   ├── base.py       # Step Protocol/ABC
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── validate.py
│   └── pipeline/         # 👈 Orchestrators (compose steps)
│       ├── __init__.py
│       ├── base.py
│       └── order_ingestion.py
├── infrastructure/
│   ├── adapter/
│   │   ├── source/       # 👈 Data sources
│   │   │   ├── s3.py
│   │   │   ├── kafka.py
│   │   │   └── postgres.py
│   │   └── sink/         # 👈 Data destinations
│   │       ├── bigquery.py
│   │       └── elasticsearch.py
│   ├── config/
│   └── client/           # External API clients
├── presentation/
│   └── cli/              # 👈 Primary entry point for pipelines
│       ├── __init__.py
│       └── run.py
└── shared/
│   ├── constant/
│   ├── exception/
│   └── typing/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── property/         # 👈 Property-based tests (Hypothesis)
├── benchmarks/           # 👈 Performance regression tests
├── docs/
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

---

## Python Framework

```
mylib-repo/
├── src/
│   └── mylib/            # 👈 Package lives here (src layout)
│		├── __init__.py             # Public API exports
|		├── _version.py             # Single source of version
|		│
|		├── core/                   # 👈 Core algorithms, hot path
|		│   ├── __init__.py
|		│   ├── _array.py           # Internal implementation
|		│   ├── _computation.py
|		│   └── _simd.py            # Low-level optimizations
|		│
|		├── api/                    # 👈 Public-facing modules
|		│   ├── __init__.py
|		│   ├── array.py            # User-facing Array class
|		│   ├── linalg.py           # np.linalg equivalent
|		│   └── random.py           # np.random equivalent
|		│
|		├── typing/                 # 👈 Type definitions, protocols
|		│   ├── __init__.py
|		│   ├── dtypes.py
|		│   └── protocols.py
|		│
|		├── _internal/              # 👈 Private utilities (underscore = private)
|		│   ├── __init__.py
|		│   ├── validation.py       # Input validation (TypeGuards)
|		│   ├── dispatch.py         # Function dispatch logic
|		│   └── compat.py           # Python version compatibility
|		│
|		├── exceptions.py           # 👈 Public exceptions
|		│
|		└── constants.py            # 👈 Public constants (dtypes, etc.)
├── tests/
│   ├── unit/
│   ├── integration/
│   └── property/         # 👈 Property-based tests (Hypothesis)
├── benchmarks/           # 👈 Performance regression tests
├── docs/
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

---
