# ADR 002: Modular Composable Skills Architecture and Flat Directory Structure

**Date:** 2026-09-13
**Status:** Accepted (Supersedes ADR 001)

## Context

Prior to this decision, skills were arranged in a two-level nested hierarchy (`skills/<domain>/<domain>-<role>/`, e.g. `skills/python-app/python-app-developer/`). This structure introduced several issues:

1. **Monolithic Duplication**: Universal Python development standards—including the Power of 10 safety rules, Behavioral TDD (Red-Green-Refactor), Vanilla BDD with Pytest (Given/When/Then), Hypothesis property testing, commit discipline, and `uv` tooling—were duplicated across multiple developer roles (`python-app-developer`, `python-game-developer`, `gymnasium-env-developer`).
2. **Coupled Product Ownership**: Product Owner practices (INVEST user stories, acceptance criteria, Kanban workflow) were entangled with storage backends across seven separate skills (`shared-project-owner-todo`, `shared-project-owner-github`, `python-app-project-owner-glab`, etc.).
3. **Redundant Pathing**: Path names were excessively deep and redundant (e.g. `skills/data-pipeline/data-pipeline-data-engineer`).

## Decision

We have adopted a modular, composable skills architecture with a single-level flat directory structure:

1. **Foundational & Domain Role Decomposition**:
   - Extracted universal core standards into **`python-developer`**, **`product-owner`**, and **`game-designer`**.
   - Specialized capabilities extend their foundation via clear frontmatter metadata (`depends_on:`):
     - `python-hexagonal`, `python-raylib`, `gymnasium-env`, `data-engineer`, `data-scientist` extend `python-developer`.
     - `rl-data-scientist` extends `python-developer` and `gymnasium-env`.
     - `backlog-todo`, `backlog-github`, and `backlog-gitlab` extend `product-owner`.
2. **Decoupled Backlog Storage Providers**:
   - Story authoring and definition of done live in `product-owner`.
   - Tooling-specific storage mechanisms (`backlog-todo` for `TODO.md`, `backlog-github` for `gh` CLI, `backlog-gitlab` for `glab` CLI) operate as independent plugins.
3. **Flat Directory Layout**:
   - All 21 skills reside directly in `skills/<skill-name>/`.
4. **Frontmatter Metadata**:
   - Every skill specifies `tags:` (keywords for discovery) and `depends_on:` (list of required parent/companion skills).
5. **Tooling**:
   - `scripts/lint_skills.py` validates flat paths, frontmatter tags, dependencies, and relative links.
   - `scripts/catalog_skills.py` provides tag and dependency-based search.

## Consequences

- **Positive:**
  - **Single Source of Truth:** Core Python rules and agile requirements standards are defined once and inherited everywhere.
  - **Composability:** Agents can dynamically load exactly what they need (e.g. `python-developer` + `gymnasium-env` + `python-raylib`).
  - **Discoverability:** Standardized tags enable searching and filtering skills independently of filesystem structure.
  - **Simplicity:** Cleaner, shorter filesystem paths (`skills/python-developer/`).
- **Negative:**
  - **Breaking Change:** Previous references to nested paths (`skills/<domain>/...`) must be updated.

## Alternatives Considered

- **Retaining Nested Folders with Shared Base**: Retaining `skills/<domain>/` while symlinking shared files. Rejected because nested paths remain redundant and fail to solve cross-domain skill composition.
- **Single Mega-Skills**: Combining app, game, and RL into one large Python skill. Rejected because specialized rules (like Raylib rendering or gym.Env spaces) would clutter unrelated projects.
