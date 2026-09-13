# ADR 008: Project Scaffolding and Architecture Templating with Copier

**Date:** 2026-09-13  
**Status:** Accepted

## Context

The Skills repository provides specialized domain instructions, architectural standards, and safety constraints for AI agents and human developers. However, starting a new project that embodies these architectural principles was historically friction-heavy:

1. **Manual Bootstrapping:** Developers and AI agents had to manually assemble directory layouts, `pyproject.toml` configurations, and `justfile` recipes, often leading to subtle inconsistencies and missing safety constraints.
2. **Missing Agent Guidance:** Newly scaffolded projects lacked an embedded `AGENTS.md`, meaning AI assistants lacked immediate domain awareness and architectural rules for that project archetype.
3. **Configuration Drift:** Without standardized templates, projects diverged in linting rules, testing setups, and dependency configurations.
4. **Monorepo Complexity:** Domain patterns like RL environments require clean separation between headless simulations and agent policies (`skills/gymnasium-env/references/structure.md`), which is error-prone to configure manually as a `uv` workspace.

We needed a standardized project templating and scaffolding system that:
- Executes directly from remote Git without prior tool installation (`uvx`-compatible).
- Supports dynamic question prompting and parameterization (project name, author, backlog provider).
- Embeds project-tailored `AGENTS.md` instructions and installs recommended skills via the open standard (`npx skills`).
- Supports both single-package applications and multi-package `uv` workspace monorepos.

---

## Decision

We adopt **[Copier](https://copier.readthedocs.io/)** as the repository-wide templating engine, executed via Astral `uvx`, organized into specialized archetypes with automated integration testing:

### 1. Templating Engine: Copier via `uvx`
- Executable on-demand with zero persistent tool installation:
  ```bash
  uvx copier copy gh:RomualdRousseau/Skills <destination>
  # Or with direct archetype selection:
  uvx copier copy -d template_type=python-app gh:RomualdRousseau/Skills <destination>
  ```
- Copier provides native Git source loading, interactive prompting, Jinja2 template rendering, and lifecycle update capabilities (`copier update`).

### 2. Multi-Archetype Dispatcher (`copier.yaml`)
A single root `copier.yaml` acts as a dispatcher prompting the user for the archetype and delegating to specialized template subdirectories under `templates/`:
- **`python-app`**: Hexagonal architecture with domain models (`__slots__`), protocol ports, application services, and infrastructure adapters.
- **`python-game`**: Decoupled game simulation with a Raylib visual rendering loop (`import pyray as pr`).
- **`data-pipeline`**: Medallion architecture (raw, core_model, business_view) using Polars, DuckDB, and Pydantic boundary validation.
- **`gymnasium-env`**: Farama Gymnasium `uv` workspace monorepo splitting `packages/env` (headless simulation, pure physics, bounded reward shaping, Raylib rendering) and `packages/agents` (random/heuristic baselines, multi-seed evaluator, trainer).

### 3. Embedded `AGENTS.md` & Recommended Skills (`npx skills`)
Every generated template embeds:
- A tailored `AGENTS.md` specifying active skills, architectural invariants, and verification workflows.
- A `just setup-skills` recipe that runs `npx skills add RomualdRousseau/Skills --skill ...` to equip AI coding assistants with the exact skills required for the project.

### 4. Continuous Template Verification Harness
To ensure templates never rot or drift:
- `scripts/test_templates.py` automatically instantiates all four templates in isolated temporary environments.
- Verifies directory structures, executes test suites (`uv run pytest`), and checks formatting and linting (`ruff check`, `ruff format --check`).
- Integrated into `just test-templates` and repository CI.

---

## Consequences

### Positive
- **Zero-Friction Instantiation:** New projects can be bootstrapped anywhere with a single `uvx copier copy` command.
- **Day-1 High Integrity:** Scaffolded projects are immediately runnable and pass all strict linting (`ruff`) and test suites (`pytest`).
- **AI Agent Alignment:** Scaffolded projects contain immediate guidance (`AGENTS.md`) and pre-wired skill dependencies installable via `just setup-skills`.
- **Maintainability & Evolution:** Copier tracks answers in `.copier-answers.yml`, allowing downstream projects to receive updates via `copier update`.

### Negative
- **Jinja Escaping Overhead:** Creating and maintaining templates containing Jinja templates requires escaping expressions and jinja extensions (`.jinja`).
- **Testing Runtime:** Testing all templates via `just test-templates` takes 10–15 seconds to clone, instantiate, sync `uv` environments, and execute pytest.

---

## Alternatives Considered

1. **Cookiecutter:**
   - *Pros:* Highly mature and widely recognized in the Python ecosystem.
   - *Cons:* Lacks native support for updating existing projects after scaffolding, lacks modern multi-template dispatch in a single repository, and requires external plugins like `cruft`.
2. **Cruft:**
   - *Pros:* Adds update capabilities to Cookiecutter.
   - *Cons:* Adds an additional wrapper layer on top of Cookiecutter, whereas Copier natively handles updates and migrations with cleaner configuration.
3. **Yeoman / Projen:**
   - *Pros:* Powerful code generation ecosystems.
   - *Cons:* Rely heavily on Node.js/npm ecosystems, introducing unwanted runtime dependencies in a Python-first repository.
4. **Static Template Folders / Raw Git Clones:**
   - *Pros:* Simple to copy manually.
   - *Cons:* Cannot dynamically parametrize package names, author details, or backlog providers (GitHub vs GitLab vs TODO). Highly prone to bitrot and configuration drift.
