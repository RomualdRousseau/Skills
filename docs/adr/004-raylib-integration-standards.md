# ADR 004: Raylib Integration Standards

**Date:** 2026-04-15
**Status:** Accepted

## Context
The `raylib` Python ecosystem has a naming discrepancy where the package is installed via `pip install raylib` but imported as `import pyray`. This often causes confusion for new developers and inconsistency in codebases.

## Decision
We will standardize the Raylib integration:
1.  **Installation:** Always use `uv add raylib`.
2.  **Import:** Always use `import pyray as pr`.
3.  **Naming:** Use the `pr` alias for all Raylib function calls to ensure brevity and consistency across the workspace.

## Consequences
- **Positive:**
  - **Consistency:** All developers and agents use the same alias, making code reviews and pair programming easier.
  - **Clarity:** The `pr` alias clearly distinguishes Raylib calls from standard Python or project-specific logic.
- **Negative:**
  - **External Examples:** Most online Raylib C examples use the full name; developers must remember to translate `InitWindow` to `pr.init_window`.
