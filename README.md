# Skills Repository

A high-integrity framework for building specialized AI environments and robust Python applications using **AI agents**.

## 🚀 Getting Started

This repository contains a suite of **Modular, Composable Skills** designed to guide AI agents through complex engineering, research, and design tasks. These skills enforce the "Power of 10" safety rules, clean architecture, and rigorous testing practices.

### 1. Flat & Composable Organization

Skills reside in a flat directory hierarchy directly under `skills/<skill-name>/`. Skills are designed to be composable: a foundational skill (such as `python-developer` or `product-owner`) can be combined with specialized domain extensions (such as `gymnasium-env`, `python-raylib`, or `backlog-github`).

### 2. Composing Skills for Your Use Case

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

### 3. Project Templates (Copier)

This repository provides zero-install project templates powered by [Copier](https://copier.readthedocs.io/) and Astral `uv`. Each template includes an embedded `AGENTS.md` pre-configured with the corresponding skills, Power of 10 safety rules, BDD tests, and `just` commands.

To scaffold a new project directly from this git repository:

```bash
# Interactive selection (prompts for template type and configuration)
uvx copier copy gh:RomualdRousseau/Skills my-project

# Or scaffold a specific template non-interactively
uvx copier copy -d template_type=python-app gh:RomualdRousseau/Skills my-app
uvx copier copy -d template_type=python-game gh:RomualdRousseau/Skills my-game
uvx copier copy -d template_type=data-pipeline gh:RomualdRousseau/Skills my-pipeline
uvx copier copy -d template_type=gymnasium-env gh:RomualdRousseau/Skills my-env
```

| Template | Embedded Skills & Architecture | Verification |
|---|---|---|
| **`python-app`** | `python-developer` + `python-hexagonal` (Ports & Adapters, CQRS) | `just check` |
| **`python-game`** | `python-developer` + `python-raylib` + `game-designer` (Headless physics & Raylib) | `just check` |
| **`data-pipeline`** | `python-developer` + `data-engineer` (Medallion Bronze/Silver/Gold, Polars, DuckDB) | `just check` |
| **`gymnasium-env`** | `python-developer` + `gymnasium-env` (Farama Gym API, Raylib render, Fire CLI) | `just check` |

### 4. Installing Skills into Existing Projects (`npx skills`)

All skills in this repository follow the open [Agent Skills](https://skills.sh/) standard (`SKILL.md`). You can install any skill directly into your existing project or editor using the `npx skills` CLI:

```bash
# Install a single skill from this repository
npx skills add RomualdRousseau/Skills --skill python-developer

# Install multiple composable skills together
npx skills add RomualdRousseau/Skills --skill python-developer --skill python-hexagonal

# Target a specific AI coding agent (e.g. claude-code, cursor)
npx skills add RomualdRousseau/Skills --skill python-developer -a claude-code
```

The CLI downloads the selected skills into `.agents/skills/<skill-name>/`, where modern AI coding agents automatically discover and load their instructions and rules.

### 5. Activating a Skill

Reference the skill by name when working with your agent:

```bash
/python-developer
/gymnasium-env
```

### 6. Following the Development Lifecycle

All development follows a strict **Research -> Strategy -> Execution** lifecycle:

1. **Research:** The agent maps the codebase and validates all assumptions.
2. **Strategy:** The agent proposes a grounded plan based on the research.
3. **Execution:** The agent implements the plan using the iterative **Plan -> Act -> Validate** cycle.

---

## 🛠️ Available Skills

### Core Python & Extensions

- **`python-developer`**: Universal foundation for high-integrity Python. Enforces the **Power of 10** rules, Behavioral TDD, Vanilla BDD with Pytest, Hypothesis property testing, and `uv` tooling.
- **`python-hexagonal`**: Hexagonal Architecture (Ports and Adapters), CQRS separation, and pure domain modeling.
- **`python-raylib`**: 2D graphics and simulation using Raylib (`pyray`), with headless engine injection and decoupled drawing protocols.
- **`gymnasium-env`**: Reinforcement learning environments conforming to the Farama Foundation Gymnasium API.
- **`data-engineer`**: High-integrity data engineering using the Medallion Hexagonal Architecture, Polars, DuckDB, and Pydantic.
- **`data-scientist`**: Fast-tracked data exploration and ML using `uv` virtualenvs and interactive Jupyter Notebooks.
- **`rl-data-scientist`**: MDP formulation (observations, actions, rewards), experiment tracking (WandB/MLflow), and Optuna hyperparameter sweeps.

### Design, Product Ownership & Backlog Tracking

- **`product-owner`**: Core agile product ownership, INVEST user story authoring, acceptance criteria formulation, and Kanban lifecycle.
- **`game-designer`**: Game design and user experience principles focusing on game feel, visual feedback, juiciness, and playability.
- **`backlog-todo`**: Local Markdown backlog tracking via `TODO.md`.
- **`backlog-github`**: GitHub Issues and Projects tracking via the `gh` CLI.
- **`backlog-gitlab`**: GitLab Issues and milestone tracking via the `glab` CLI.

### Systems, Documentation & Cross-Cutting

- **`ai-architect`**: RAG patterns, prompt engineering, context management, and LLM evaluation with Ragas.
- **`observability`**: Production observability standards covering OpenTelemetry (OTel), structured JSON logging, and SLI/SLO metrics.
- **`security-audit`**: Security audit standards, SAST/DAST automation, OWASP Top 10 mitigation, and secret scanning.
- **`technical-writer`**: Architecture Decision Records (ADRs), Mermaid.js diagrams, and API documentation.
- **`presentation-html`**: HTML5 and Tailwind CSS widescreen presentation generator with Playwright screenshots and PDF compilation.
- **`presentation-svg`**: Direct vector SVG presentation generator producing editable PowerPoint decks and PDF exports.
- **`variant-analysis`**: Automated genomic variant analysis (VEP) and clinical assessment using multi-agent systems.
- **`devops-gcp`**: Cloud infrastructure automation for GCP using Terraform, Workload Identity Federation (WIF), and GitLab CI/CD.
- **`llm-wiki`**: Knowledge base and documentation management using Markdown wikis optimized for LLMs.

---

## 🔍 Discovery Tooling

Use `scripts/catalog_skills.py` to search and inspect skills by capability or tag:

```bash
# List all skills with dependencies and tags
python scripts/catalog_skills.py

# Filter skills by tag
python scripts/catalog_skills.py --tag rl
python scripts/catalog_skills.py --tag python

# Inspect a specific skill and its dependency hierarchy
python scripts/catalog_skills.py --skill rl-data-scientist
```

---

## 🏗️ Architectural Foundations

### The "Power of 10" Safety Rules

All Python development adheres to these ten rules:

1. **No Recursion**: Use iterative stacks.
2. **Hard Loop Bounds**: Every `while` loop must have a `MAX_ITERATIONS`.
3. **Memory Discipline**: Use `__slots__` for domain models.
4. **Boundary Validation**: Use `TypeGuards` at entry points.
5. **Pure Functions**: Business logic must be side-effect free.
6. **Dependency Injection**: Pass, don't construct, collaborators.
7. **No Magic**: Forbidden use of `eval()`, `exec()`, or `getattr()`.
8. **Protocol Interfaces**: Decouple layers with `typing.Protocol`.
9. **Fail-Closed**: Logic must default to "abort" on ambiguity.
10. **Test the Invariants**: Use property-based testing (Hypothesis).

### ADR Process

Significant technical decisions are recorded in `docs/adr/`. When proposing major architectural changes:
1. Draft a new ADR using `skills/technical-writer/references/adr-template.md`.
2. Review the ADR with stakeholders.
3. Commit the decision for long-term project context.

---

## 🤝 Credits

- **`llm-wiki`**: Inspired by [Andrej Karpathy's gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki).
- **`presentation-html`**: Credits to [Kévin François-Bouaou, PhD](https://fr.linkedin.com/in/kevin-fran%C3%A7ois-bouaou-phd).

---

## 📄 License

See `LICENSE` for details.
