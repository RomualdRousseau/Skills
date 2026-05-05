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

### Behavioral TDD (Application Layer)

All business logic in the `application/` layer must be developed using a **Test-First** approach:

1.  **Red**: Write a failing test that defines the expected behavior.
2.  **Green**: Implement the minimum code to pass the test.
3.  **Refactor**: Clean up the code while ensuring tests stay green.

### Vanilla BDD with Pytest

Use standard `pytest` functions structured by behavior. Every test must follow the **Given / When / Then** pattern to ensure readability and focus on requirements:

- **Given**: The initial context, state, or mock setup.
- **When**: The specific action or event being tested.
- **Then**: The expected outcome, side effect, or invariant check.

### Systematic Bug Reproduction

If a bug is reported, a fix is incomplete without a reproduction test:

1.  Create a test case that reproduces the reported bug (it must fail in the current state).
2.  Implement the fix.
3.  Verify the test now passes. The test remains in the main suite as a permanent regression safeguard.

### Technical Standards

- **Property-Based Testing**: Use `Hypothesis` to test invariants (e.g., "Unauthorized" state cannot be flipped by any string input).
- **Strict Mocking**: All mocks must use `spec=True` to ensure they adhere to the real interface.
- **100% Logic Coverage**: Pure functions in the `application` layer must have exhaustive unit test coverage via TDD.


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
├── infrastructure/
|	│   ├── adapter/        # Implementations (Bounded loops)
|	│   └── config/         # Environment variables & secrets (Injected only)
|	├── presentation/
|	│   ├── api/            # TypeGuards & Handlers
|	│   └── cli/            # Entry points
|	├── shared/
|	│   ├── constant/       # Single source of truth for all constants
|	│   └── exception/      # Custom Fail-Closed exceptions
```

## 6. Configuration & Constants

### Constants (`shared/constant/`)
Constants are **Immutable Truths** that are globally valid across all layers. To avoid fragmentation, all business constants and technical safety bounds live here.
- **Import Policy**: Can be imported by any layer.
- **Examples**: `TAX_RATE`, `MAX_ITERATIONS`, `SUPPORTED_LANGUAGES`.

### Configuration (`infrastructure/config/`)
Configuration represents **Environmental Variables** that change based on the deployment context (Dev/Prod).
- **Import Policy**: **Forbidden in the `application/` layer**. Business logic must remain environment-agnostic.
- **Injection Pattern**: Values from `infrastructure/config/` must be injected into services via their constructors at the `presentation/` or `composition` root.
- **Examples**: `DATABASE_URL`, `STRIPE_API_KEY`, `LOG_LEVEL`.

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

