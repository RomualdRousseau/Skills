# Agent Guidance: Using the Skills Repository

This document provides instructions for AI agents on how to load, activate, and compose the skills defined in this repository.

## What This Repository Is

This is a **modular skill library** — a collection of specialized domain instructions, architectural standards, and workflows. Skills are organized in a flat structure (`skills/<skill-name>/`) and designed to be composed together using explicit dependencies (`depends_on:`) and discoverable tags (`tags:`).

## How to Load and Activate Skills

### 1. Direct File Loading

Skills are located in `skills/<skill-name>/SKILL.md`. To activate a skill:

1. **Read** the `SKILL.md` file for the skill you need.
2. **Read dependencies**: If the skill specifies parent skills in `depends_on:`, load and enforce those as well.
3. **Adopt** the role, rules, and workflows described in those files.
4. **Follow** the standards for the duration of the current task.

Example: To act as a Gymnasium RL developer, load `skills/python-developer/SKILL.md` and `skills/gymnasium-env/SKILL.md` (and `skills/python-raylib/SKILL.md` if visualization is required).

### 2. Composable Skill Recipes

| Goal / Role | Skills to Activate |
|---|---|
| **Gymnasium RL Developer** | `python-developer` + `gymnasium-env` (+ `python-raylib` if visual) |
| **Python Game Developer** | `python-developer` + `python-raylib` |
| **Backend / Web App Developer** | `python-developer` + `python-hexagonal` |
| **Data Engineer (Pipelines & Medallion)** | `python-developer` + `data-engineer` |
| **Data Scientist (Notebooks & EDA)** | `python-developer` + `data-scientist` |
| **RL Data Scientist (MDP & Sweeps)** | `python-developer` + `gymnasium-env` + `rl-data-scientist` |
| **Game Designer (with GitHub Backlog)** | `game-designer` + `product-owner` + `backlog-github` |
| **Game Designer (with TODO Backlog)** | `game-designer` + `product-owner` + `backlog-todo` |
| **Project Owner (GitHub Issues)** | `product-owner` + `backlog-github` |
| **Project Owner (GitLab Issues)** | `product-owner` + `backlog-gitlab` |
| **Project Owner (Local TODO.md)** | `product-owner` + `backlog-todo` |

### 3. Activation by Natural Language Trigger

Each `SKILL.md` includes a **Project Interaction** section with natural language triggers:
- **"Implement the domain model for User"** → Load `python-developer` + `python-hexagonal`
- **"Draft an ADR for using Redis"** → Load `technical-writer`
- **"Design a RAG pipeline"** → Load `ai-architect`
- **"Manage project backlog or user stories"** → Load `product-owner` + `backlog-github` (or `backlog-todo`)
- **"Build an RL environment for drone simulation"** → Load `python-developer` + `gymnasium-env`
- **"Develop an idempotent ETL pipeline"** → Load `python-developer` + `data-engineer`

### 4. Activation by Command Prefix

If your framework supports command-based skill activation, use the skill name as defined in the frontmatter:
```
/python-developer
/python-hexagonal
/gymnasium-env
/product-owner
/backlog-github
```

## Project Scaffolding via Templates (Copier)

To scaffold a new high-integrity project with an embedded `AGENTS.md` and complete testing harness:

```bash
# Interactive template wizard
uvx copier copy gh:RomualdRousseau/Skills <destination>

# Direct template instantiation
uvx copier copy -d template_type=python-app gh:RomualdRousseau/Skills <destination>
uvx copier copy -d template_type=python-game gh:RomualdRousseau/Skills <destination>
uvx copier copy -d template_type=data-pipeline gh:RomualdRousseau/Skills <destination>
uvx copier copy -d template_type=gymnasium-env gh:RomualdRousseau/Skills <destination>
```

Each generated project contains an embedded `AGENTS.md` tailored specifically to that project's architecture and active skills. After scaffolding, developers and agents can install recommended skills using `just setup-skills` (which runs `npx skills add RomualdRousseau/Skills --skill ...`).

## Standard Development Lifecycle

All skills follow this lifecycle:

### 1. Research
- Map the codebase and validate all assumptions.
- Read relevant `SKILL.md` and reference files.
- Do not write code until you understand the context.

### 2. Strategy
- Propose a grounded plan based on your research.
- For significant architectural changes, draft an ADR using `skills/technical-writer/references/adr-template.md`.
- Seek approval before proceeding if the change is major.

### 3. Execution
- Implement the plan using the iterative **Plan → Act → Validate** cycle.
- Follow the rules and constraints of all active skills.
- Commit changes semantically and frequently.

## Shared Engineering Standards

### The "Power of 10" Safety Rules
1. **No Recursion:** Use iterative stacks.
2. **Hard Loop Bounds:** Every `while` loop must have a `MAX_ITERATIONS`.
3. **Memory Discipline:** Use `__slots__` for domain models.
4. **Boundary Validation:** Use `TypeGuards` at entry points.
5. **Pure Functions:** Business logic must be side-effect free.
6. **Dependency Injection:** Pass, don't construct, collaborators.
7. **No Magic:** Forbidden use of `eval()`, `exec()`, or `getattr()` for sensitive logic.
8. **Protocol Interfaces:** Decouple layers with `typing.Protocol`.
9. **Fail-Closed:** Logic must default to "abort" on ambiguity.
10. **Test the Invariants:** Use property-based testing (Hypothesis).

### Architecture Decision Records (ADR)
- Significant technical decisions are recorded in `docs/adr/`.
- Use the standard ADR template: `skills/technical-writer/references/adr-template.md`.

## Complete Skill Catalog

| Skill | Location | Dependencies | Tags |
|---|---|---|---|
| `python-developer` | `skills/python-developer/` | - | `python`, `development`, `tdd`, `power-of-10`, `clean-code` |
| `python-hexagonal` | `skills/python-hexagonal/` | `python-developer` | `python`, `architecture`, `hexagonal`, `ddd`, `ports-and-adapters` |
| `python-raylib` | `skills/python-raylib/` | `python-developer` | `python`, `game`, `raylib`, `graphics`, `simulation` |
| `gymnasium-env` | `skills/gymnasium-env/` | `python-developer` | `rl`, `gymnasium`, `simulation`, `python`, `environment` |
| `data-engineer` | `skills/data-engineer/` | `python-developer` | `data-engineering`, `medallion`, `polars`, `duckdb`, `pydantic`, `pipeline`, `python` |
| `data-scientist` | `skills/data-scientist/` | `python-developer` | `data-science`, `jupyter`, `exploration`, `analysis`, `machine-learning`, `python` |
| `rl-data-scientist` | `skills/rl-data-scientist/` | `python-developer`, `gymnasium-env` | `rl`, `mdp`, `data-science`, `evaluation`, `optuna`, `python` |
| `game-designer` | `skills/game-designer/` | - | `game-design`, `mechanics`, `fun-factor`, `ux` |
| `product-owner` | `skills/product-owner/` | - | `agile`, `product-management`, `user-stories`, `backlog`, `requirements` |
| `backlog-todo` | `skills/backlog-todo/` | `product-owner` | `backlog`, `todo`, `markdown`, `kanban`, `tracking` |
| `backlog-github` | `skills/backlog-github/` | `product-owner` | `github`, `cli`, `issues`, `projects`, `backlog`, `tracking` |
| `backlog-gitlab` | `skills/backlog-gitlab/` | `product-owner` | `gitlab`, `cli`, `issues`, `backlog`, `tracking` |
| `variant-analysis` | `skills/variant-analysis/` | `python-developer`, `data-scientist` | `genomics`, `bioinformatics`, `vep`, `vcf`, `science`, `python` |
| `devops-gcp` | `skills/devops-gcp/` | - | `devops`, `gcp`, `terraform`, `gitlab-ci`, `infrastructure` |
| `security-audit` | `skills/security-audit/` | - | `security`, `sast`, `dast`, `owasp`, `audit` |
| `observability` | `skills/observability/` | - | `observability`, `opentelemetry`, `logging`, `metrics`, `tracing`, `reliability` |
| `technical-writer` | `skills/technical-writer/` | - | `documentation`, `technical-writing`, `adr`, `mermaid`, `architecture` |
| `presentation-html` | `skills/presentation-html/` | - | `presentation`, `html`, `tailwind`, `slides`, `pdf` |
| `presentation-svg` | `skills/presentation-svg/` | - | `presentation`, `svg`, `pptx`, `slides`, `vector` |
| `ai-architect` | `skills/ai-architect/` | - | `ai`, `llm`, `rag`, `prompt-engineering`, `evaluation` |
| `llm-wiki` | `skills/llm-wiki/` | - | `knowledge-base`, `wiki`, `documentation`, `llm`, `markdown` |

## Discovery Tooling

Use `scripts/catalog_skills.py` to search and inspect skills:
```bash
# List all skills with dependencies and tags
python scripts/catalog_skills.py

# Filter skills by tag
python scripts/catalog_skills.py --tag rl
python scripts/catalog_skills.py --tag python

# Show full details and dependency tree for a skill
python scripts/catalog_skills.py --skill rl-data-scientist
```

## File Conventions

- **SKILL.md**: The primary skill definition with YAML frontmatter (`name`, `description`, `tags`, `depends_on`).
- **references/**: Supporting documents, standards, and templates.
- **evals/**: Evaluation test suites and assertions (`evals.json`) adhering to `agentskills.io`.
- **scripts/**: Automation and helper scripts.
- **assets/**: Reusable boilerplate files (`.gitignore`, `pre-commit-config.yaml`, `justfile`).

## Skill Quality & Evaluation (agentskills.io)

Skills in this repository support automated evaluation based on the open [agentskills.io specification](https://agentskills.io/skill-creation/evaluating-skills.md):
- **Evaluation Suites:** Stored in `skills/<skill-name>/evals/evals.json` containing test cases (`id`, `prompt`, `expected_output`) and objective `assertions`.
- **Validation:** Run `just lint-evals` to validate all evaluation suites against the specification.
- **Scaffolding:** Run `just scaffold-evals <skill-name>` to generate starter test cases.
- **Benchmarking & Uplift:** Run `just benchmark-evals <dir>` and `just report-evals <dir>` to calculate empirical uplifts (`pass_rate`, execution time, tokens).
- **Benchmark Report:** After evaluating a skill, `BENCHMARK.md` must be updated with the evaluation summary and metrics.
- See [`docs/skill-evaluation.md`](file:///home/romuald/Projects/Perso/Skills/docs/skill-evaluation.md) for complete guidelines.

## Agent Rules

1. **Always load the skill** before executing a task that matches the skill's domain.
2. **Enforce the skill's rules** throughout the task. Do not silently drop constraints.
3. **Read references** when a skill points to them. They contain critical standards and templates.
4. **Draft ADRs** for significant architectural decisions using the `technical-writer` skill.
5. **Stay in role** until the task is complete or the user explicitly asks you to switch roles.
6. **Use the `product-owner` skill** in conjunction with `backlog-github` or `backlog-todo` when starting new projects or managing backlogs.
7. **Create User Stories on GitHub**: Before making any code modification or file edit, you must create a corresponding User Story as an issue on GitHub using the `gh` CLI (`gh issue create`). The story must have clear Acceptance Criteria.
8. **Mark Stories as Done**: Once the changes are fully implemented and verified (passing `just lint`), you must immediately close the issue representing that story using `gh issue close <id>`.
9. **Update BENCHMARK.md**: After evaluating any skill, you must update `BENCHMARK.md` with the evaluation summary, baseline/skill pass rates, and uplift metrics.
