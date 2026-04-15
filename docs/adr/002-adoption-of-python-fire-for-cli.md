# ADR 002: Adoption of python-fire for CLI Implementation

**Date:** 2026-04-15
**Status:** Accepted

## Context

Building Gymnasium environments requires several distinct entry points: human play mode (for debugging), environment testing (random agent), and various agent training/evaluation modes. Manual `argparse` implementations are verbose and error-prone.

## Decision

We will adopt `python-fire` as the standard library for implementing CLIs in Gymnasium environments. This allows us to expose class methods (e.g., `play`, `test_env`, `train`) directly as CLI commands with minimal boilerplate.

## Consequences

- **Positive:**
  - **Rapid Prototyping:** New methods added to the `CLI` class are automatically available as commands.
  - **Standard Interface:** All environments share the same command structure (`play`, `test-env`, `train`).
  - **Readability:** CLI logic is kept clean and declarative.
- **Negative:**
  - **Dynamic Nature:** `fire` relies on reflection, which can occasionally hide errors until runtime compared to more static libraries like `click`.
