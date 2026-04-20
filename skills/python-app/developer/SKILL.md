---
name: developer
description: This skill serves as the source of truth for high-integrity Python development, focusing on safety, determinism, and hexagonal architecture.
---

## 1. Architectural Integrity

### Hexagonal Structure

All code must be organized into three distinct layers to ensure separation of concerns and testability:

- **`presentation/`**: Entry points (API, CLI). Responsible for input validation via `TypeGuards`.
- **`application/`**: Pure business logic and orchestration. Defines `Protocols` (Ports).
- **`infrastructure/`**: External implementations (DB, LLM, API clients). Implements `Protocols` (Adapters).

### Design Principles

- **Fail-Closed:** Logic must default to "Access Denied" or "Operation Aborted" upon any exception or ambiguity.
- **Composition Over Inheritance:** Maximum 2 levels of inheritance. Use `Protocols` for flexibility and `ABCs` only for strict enforcement.
- **Late Abstraction:** Do not define interfaces/Protocols until at least two concrete implementations exist.
- **Singular Naming:** Use singular package names (e.g., `model`, `service`, `adapter`).
- **Light CQRS:** Explicitly separate "State-Changing" operations from "State-Reading" operations.
    - **Commands:** Methods that change state should be named with verbs (e.g., `create_user`, `update_order`). They must return `None` or a simple `Success/Failure` status.
    - **Queries:** Methods that read state must start with `get_`, `list_`, or `check_`. They must be side-effect free and return data (models or DTOs).

## 2. Control & Safety (The Power of 10)

1. **No Recursion:** All tree or graph traversals (especially LLM JSON parsing) must use iterative stacks.
2. **Hard Loop Bounds:** Every `while` loop must be guarded by `MAX_ITERATIONS` or `TIMEOUT_SECONDS`.
3. **Memory Discipline:** Use `__slots__` for high-throughput classes to ensure deterministic memory usage.
4. **Validation at Boundary:** Use `TypeGuard` at the `presentation` layer. Internal layers assume data is valid.
5. **Pure Functions:** Business logic must be I/O-free and deterministic. Side effects are pushed to the `infrastructure` edges.
6. **Dependency Injection:** Collaborators must be passed in, never instantiated internally.
7. **No Magic:** Forbidden: `eval()`, `exec()`, `getattr()` for sensitive logic, and dynamic imports.
8. **Immutable Invariants:** Security states must be provably immutable against malformed input.

## 3. Testing & Verification

- **Property-Based Testing:** Use `Hypothesis` to test invariants (e.g., "Unauthorized" state cannot be flipped by any string input).
- **Strict Mocking:** All mocks must use `spec=True` to ensure they adhere to the real interface.
- **100% Logic Coverage:** Pure functions in the `application` layer must have exhaustive unit test coverage.

## 4. Operational Workflow

### Commit Discipline

Changes are committed semantically and frequently. If a change is large, it is split in this order:

1. **Core Logic / Models** (`application/model`)
2. **Ports / Protocols** (`application/port`)
3. **Adapters / Infrastructure** (`infrastructure/adapter`)
4. **API / Presentation** (`presentation/api`)
5. **Tests & Docs**

### Conventional Commits

Format: `<type>(<scope>): <subject>`

- `feat`: New functionality.
- `fix`: Bug fix.
- `refactor`: Structural change without logic change.
- `test`: Adding or updating tests.

## 5. Project Template

```text
repo/
├── src/
|	├── application/
|	│   ├── model/          # Domain entities (__slots__ used here)
|	│   ├── port/           # Protocols (Interfaces)
|	│   └── service/        # Pure logic & orchestration
|	├── infrastructure/
|	│   ├── adapter/        # Implementations (Bounded loops)
|	│   └── config/         # Settings & Constants
|	├── presentation/
|	│   ├── api/            # TypeGuards & Handlers
|	│   └── cli/            # Entry points
|	├── shared/
|	│   ├── constant/       # MAX_ITERATIONS = 10_000
|	│   └── exception/      # Custom Fail-Closed exceptions
└── tests/
    ├── property/       # Hypothesis tests
    └── unit/           # Spec-based mocks
```

## Project Interaction

- **Trigger**: "Implement the domain model for [entity]"
- **Trigger**: "Define the Protocols and Ports for [module]"
- **Trigger**: "Refactor [module] to follow Hexagonal Architecture"
- **Trigger**: "Audit the code for Power of 10 safety rules"
- **Trigger**: "Add property-based tests for [logic]"
- **Trigger**: "Implement the [service/orchestrator] for [workflow]"

