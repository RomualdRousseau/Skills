# ADR 003: Implementation of Light CQRS

**Date:** 2026-04-15
**Status:** Accepted

## Context

In high-integrity Python applications, side effects hidden within retrieval methods can lead to non-deterministic behavior and difficult-to-reproduce bugs.

## Decision

We will implement "Light CQRS" (Command Query Responsibility Segregation) principles.

- **Commands:** Must use verbs (e.g., `update_state`) and focus on modification. They return `None` or success/failure.
- **Queries:** Must start with `get_`, `list_`, or `check_`. They must be side-effect free (idempotent) and return data.

## Consequences

- **Positive:**
  - **Predictability:** Developers can trust that a `get_` method will not modify system state.
  - **Testability:** Pure queries are trivial to unit test.
  - **Auditability:** State changes are localized to specific, verb-named "Command" methods.
- **Negative:**
  - **Verbosity:** Occasionally requires splitting a "get-and-update" operation into two distinct calls.
