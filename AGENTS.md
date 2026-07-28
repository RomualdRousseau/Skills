# Agent Guidance: Using the Skills Repository

This document provides instructions for AI agents on how to load, activate, and follow the skills defined in this repository.

## What This Repository Is

This is a **skill library** — a collection of specialized domain instructions, architectural standards, and workflows. Each skill is a self-contained set of rules and best practices for a specific engineering role (e.g., `python-app-developer`, `shared-ai-architect`, `science-data-scientist`).

## How to Load and Activate Skills

### 1. Direct File Loading

Skills are located in `skills/<domain>/<role-name>/SKILL.md`. To activate a skill:

1. **Read** the `SKILL.md` file for the skill you need.
2. **Adopt** the role, rules, and workflows described in that file.
3. **Follow** the standards for the duration of the current task.

Example: To act as a high-integrity Python developer, read `skills/python-app/python-app-developer/SKILL.md` and enforce its "Power of 10" rules and hexagonal architecture.

### 2. Skill Inheritance

Some skills **extend** others. For example:
- `skills/gymnasium-env/gymnasium-env-developer/` inherits all rules from `skills/python-app/python-app-developer/` and adds RL-specific standards.

When operating in a domain that extends another, you must enforce **both** the base skill and the specialized skill.

### 3. Activation by Natural Language Trigger

Each `SKILL.md` includes a **Project Interaction** section with natural language triggers. If the user's request matches one of these triggers, you should load the corresponding skill.

Examples:
- **"Implement the domain model for User"** → Load `skills/python-app/python-app-developer/`
- **"Draft an ADR for using Redis"** → Load `skills/shared/shared-technical-writer/`
- **"Design a RAG pipeline"** → Load `skills/shared/shared-ai-architect/`
- **"Start a new project"** → Load `skills/python-app/python-app-project-owner-todo/` or `skills/gymnasium-env/gymnasium-env-designer-todo/`

### 4. Activation by Command Prefix

If your framework supports command-based skill activation, use the skill name as defined in the frontmatter of each `SKILL.md`:

```yaml
---
name: python-app-developer
description: ...
---
```

Activation examples (syntax depends on your framework):
```
/python-app-developer
/shared-ai-architect
/science-data-scientist
```

## Standard Development Lifecycle

All skills follow this lifecycle unless overridden by a specific skill:

### 1. Research
- Map the codebase and validate all assumptions.
- Read relevant `SKILL.md` and reference files.
- Do not write code until you understand the context.

### 2. Strategy
- Propose a grounded plan based on your research.
- For significant architectural changes, draft an ADR (Architecture Decision Record) using `skills/shared/shared-technical-writer/references/adr-template.md`.
- Seek approval before proceeding if the change is major.

### 3. Execution
- Implement the plan using the iterative **Plan → Act → Validate** cycle.
- Follow the rules and constraints of the active skill.
- Commit changes semantically and frequently.

## Shared Engineering Standards

These standards apply across all skills unless explicitly overridden:

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
- Use the standard ADR template: `skills/shared/shared-technical-writer/references/adr-template.md`.
- Store decisions for long-term project context.

### Documentation Standards
- Use **Mermaid.js** for diagrams within Markdown.
- Explain **why**, not **what**, in code comments.
- Use consistent docstring formats (Google or Sphinx).

## Skill Reference

### Core Python Development
| Skill | Location | Purpose |
|-------|----------|---------|
| `python-app-developer` | `skills/python-app/python-app-developer/` | High-integrity Python, Power of 10, Hexagonal Architecture |
| `python-app-project-owner-todo` | `skills/python-app/python-app-project-owner-todo/` | Backlog, user stories, acceptance criteria |
| `python-app-project-owner-glab` | `skills/python-app/python-app-project-owner-glab/` | GitLab backlog, issues, glab CLI integration |
| `python-app-devops` | `skills/python-app/python-app-devops/` | GCP, Terraform, GitLab CI/CD |

### Gymnasium & RL Environments
| Skill | Location | Purpose |
|-------|----------|---------|
| `gymnasium-env-developer` | `skills/gymnasium-env/gymnasium-env-developer/` | Raylib, Gymnasium, Scene Pattern |
| `gymnasium-env-designer-todo` | `skills/gymnasium-env/gymnasium-env-designer-todo/` | Game design, local TODO backlog, fun factor |
| `gymnasium-env-designer-github` | `skills/gymnasium-env/gymnasium-env-designer-github/` | Game design, GitHub Issues backlog, fun factor |
| `gymnasium-env-data-scientist` | `skills/gymnasium-env/gymnasium-env-data-scientist/` | MDP design, experiments, evaluation |

### Data Engineering
| Skill | Location | Purpose |
|-------|----------|---------|
| `data-pipeline-data-engineer` | `skills/data-pipeline/data-pipeline-data-engineer/` | Polars, Pydantic, Medallion Architecture |

### Science & Exploration
| Skill | Location | Purpose |
|-------|----------|---------|
| `science-data-scientist` | `skills/science/science-data-scientist/` | Jupyter, uv, exploration |
| `science-variant-analysis` | `skills/science/science-variant-analysis/` | Genomic VEP analysis |

### Shared Cross-Cutting Skills
| Skill | Location | Purpose |
|-------|----------|---------|
| `shared-ai-architect` | `skills/shared/shared-ai-architect/` | RAG, prompt engineering, evaluation |
| `shared-llm-wiki` | `skills/shared/shared-llm-wiki/` | Knowledge management for LLM docs |
| `shared-security-audit` | `skills/shared/shared-security-audit/` | SAST/DAST, OWASP |
| `shared-observability` | `skills/shared/shared-observability/` | JSON logging, OpenTelemetry |
| `shared-technical-writer` | `skills/shared/shared-technical-writer/` | ADRs, Mermaid diagrams, docs |
| `shared-presentation-generator` | `skills/shared/shared-presentation-generator/` | Technical slides, PDFs |
| `shared-html-prez` | `skills/shared/shared-html-prez/` | HTML5/Tailwind widescreen slides |
| `shared-svg-prez` | `skills/shared/shared-svg-prez/` | SVG vector widescreen slides |
| `shared-project-owner-github` | `skills/shared/shared-project-owner-github/` | Backlog & User Story management via GitHub Issues |

## File Conventions

- **SKILL.md**: The primary skill definition. Contains role description, rules, and workflows.
- **references/**: Supporting documents, standards, and templates referenced by the skill.
- **scripts/**: Automation scripts that the skill may instruct you to run.
- **assets/**: Boilerplate files (e.g., `.gitignore`, `pre-commit-config.yaml`, `justfile`).
- **templates/**: Starter templates for new projects or documentation.

### Skill Naming & Folder Constraints

To prevent collisions when skills are imported, cached, or flattened (for instance, via `npx skills`), all skills must adhere to a strict prefixed naming convention:
- **Prefix Requirement**: Prepend the parent folder (app type or category, e.g., `python-app`, `python-game`, `shared`, `science`, `gymnasium-env`) to both the nested directory name and the `name:` attribute in the YAML frontmatter.
- **Example**: `skills/python-game/developer` with frontmatter `name: developer` must be structured and named as `skills/python-game/python-game-developer` with frontmatter `name: python-game-developer`.

## Agent Rules

1. **Always load the skill** before executing a task that matches the skill's domain.
2. **Enforce the skill's rules** throughout the task. Do not silently drop constraints.
3. **Read references** when a skill points to them. They contain critical standards and templates.
4. **Draft ADRs** for significant architectural decisions using the `shared-technical-writer` skill.
5. **Stay in role** until the task is complete or the user explicitly asks you to switch roles.
6. **Use the `python-app-project-owner-todo` or `gymnasium-env-designer-todo` skill** when starting new projects or managing backlogs.
7. **Create User Stories on GitHub**: Before making any code modification or file edit, you must create a corresponding User Story as an issue on GitHub using the `gh` CLI (`gh issue create`). The story must have clear Acceptance Criteria.
8. **Mark Stories as Done**: Once the changes are fully implemented and verified (passing `just lint`), you must immediately close the issue representing that story using `gh issue close <id>`.
