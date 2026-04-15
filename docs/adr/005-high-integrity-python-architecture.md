# ADR 005: High-Integrity Python Architecture and Code Rules

**Date:** 2026-04-15
**Status:** Accepted

## Context

Standard Python development often lacks rigorous architectural constraints, which can lead to "spaghetti" logic, hidden side effects, and non-deterministic behavior—especially in AI-driven or simulation-heavy applications. To ensure reliability, safety, and maintainability, we need a standard that enforces clear boundaries and deterministic code.

## Decision

We will adopt a High-Integrity Python Standard based on two foundational pillars:

### 1. Hexagonal Architecture (Ports & Adapters)

All applications must be structured into three distinct layers:

- **Presentation:** Entry points (API, CLI, UI) responsible for I/O and initial input validation.
- **Application (Core):** Pure business logic, orchestration, and domain models. This layer must be I/O-free and deterministic.
- **Infrastructure:** External implementations (Database, LLM clients, API adapters). This layer implements the interfaces (Ports) defined by the Application layer.

### 2. The "Power of 10" Safety Rules

Adapted for Python, we enforce:

1.  **No Recursion:** All traversals must use iterative stacks to prevent stack overflow and ensure predictability.
2.  **Hard Loop Bounds:** Every `while` loop must have a defined `MAX_ITERATIONS` or `TIMEOUT`.
3.  **Memory Discipline:** Use `__slots__` for domain models to ensure deterministic memory usage.
4.  **Boundary Validation:** Use `TypeGuards` or Pydantic at the Presentation edge.
5.  **Pure Functions:** Business logic must be free of side effects.
6.  **Dependency Injection:** Collaborators must be passed in, never instantiated internally.
7.  **No Magic:** Forbidden use of `eval()`, `exec()`, or sensitive `getattr()`.
8.  **Protocol Interfaces:** Use `typing.Protocol` for late abstraction and flexible, type-safe decoupling.

## Consequences

- **Positive:**
  - **Extreme Testability:** The pure Application layer can be tested with 100% coverage without mocks for I/O.
  - **Safety:** Hard bounds and no recursion prevent catastrophic hung processes or crashes.
  - **Portability:** Infrastructure (e.g., switching from SQLite to PostgreSQL) can be swapped without touching business logic.
- **Negative:**
  - **Higher Initial Effort:** Simple scripts require more boilerplate and architectural planning.
  - **Strictness:** Developers must explicitly manage state and dependencies, which can be more mentally taxing than "quick and dirty" Python.
