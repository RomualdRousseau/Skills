# Agent Guidance: Using the Skills Repository

This document provides instructions for AI agents on how to load, activate, and follow the skills defined in this repository.

## What This Repository Is

This is a **skill library** — a collection of specialized domain instructions, architectural standards, and workflows. Each skill is a self-contained set of rules and best practices for a specific engineering role (e.g., `developer`, `ai-architect`, `data-scientist`).

## How to Load and Activate Skills

### 1. Direct File Loading

Skills are located in `skills/<domain>/<role-name>/SKILL.md`. To activate a skill:

1. **Read** the `SKILL.md` file for the skill you need.
2. **Adopt** the role, rules, and workflows described in that file.
3. **Follow** the standards for the duration of the current task.

Example: To act as a high-integrity Python developer, read `skills/python-app/developer/SKILL.md` and enforce its "Power of 10" rules and hexagonal architecture.

### 2. Skill Inheritance

Some skills **extend** others. For example:
- `skills/gymnasium-env/developer/` inherits all rules from `skills/python-app/developer/` and adds RL-specific standards.

When operating in a domain that extends another, you must enforce **both** the base skill and the specialized skill.

### 3. Activation by Natural Language Trigger

Each `SKILL.md` includes a **Project Interaction** section with natural language triggers. If the user's request matches one of these triggers, you should load the corresponding skill.

Examples:
- **"Implement the domain model for User"** → Load `skills/python-app/developer/`
- **"Draft an ADR for using Redis"** → Load `skills/shared/technical-writer/`
- **"Design a RAG pipeline"** → Load `skills/shared/ai-architect/`
- **"Start a new project"** → Load `skills/python-app/project-owner/` or `skills/gymnasium-env/designer/`

### 4. Activation by Command Prefix

If your framework supports command-based skill activation, use the skill name as defined in the frontmatter of each `SKILL.md`:

```yaml
---
name: developer
description: ...
---
```

Activation examples (syntax depends on your framework):
```
/ai-architect
/data-scientist
/security-audit
```

## Standard Development Lifecycle

All skills follow this lifecycle unless overridden by a specific skill:

### 1. Research
- Map the codebase and validate all assumptions.
- Read relevant `SKILL.md` and reference files.
- Do not write code until you understand the context.

### 2. Strategy
- Propose a grounded plan based on your research.
- For significant architectural changes, draft an ADR (Architecture Decision Record) using `skills/shared/technical-writer/references/adr-template.md`.
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
- Use the standard ADR template: `skills/shared/technical-writer/references/adr-template.md`.
- Store decisions for long-term project context.

### Documentation Standards
- Use **Mermaid.js** for diagrams within Markdown.
- Explain **why**, not **what**, in code comments.
- Use consistent docstring formats (Google or Sphinx).

## Skill Reference

### Core Python Development
| Skill | Location | Purpose |
|-------|----------|---------|
| `developer` | `skills/python-app/developer/` | High-integrity Python, Power of 10, Hexagonal Architecture |
| `project-owner` | `skills/python-app/project-owner/` | Backlog, user stories, acceptance criteria |
| `devops` | `skills/python-app/devops/` | GCP, Terraform, GitLab CI/CD |

### Gymnasium & RL Environments
| Skill | Location | Purpose |
|-------|----------|---------|
| `developer` | `skills/gymnasium-env/developer/` | Raylib, Gymnasium, Scene Pattern |
| `designer` | `skills/gymnasium-env/designer/` | Game design, backlog, fun factor |
| `data-scientist` | `skills/gymnasium-env/data-scientist/` | MDP design, experiments, evaluation |

### Data Engineering
| Skill | Location | Purpose |
|-------|----------|---------|
| `data-engineer` | `skills/data-pipeline/data-engineer/` | Polars, Pydantic, Medallion Architecture |

### Research & Science
| Skill | Location | Purpose |
|-------|----------|---------|
| `data-scientist` | `skills/research/data-scientist/` | Jupyter, uv, exploration |
| `variant-analysis` | `skills/research/variant-analysis/` | Genomic VEP analysis |

### Shared Cross-Cutting Skills
| Skill | Location | Purpose |
|-------|----------|---------|
| `ai-architect` | `skills/shared/ai-architect/` | RAG, prompt engineering, evaluation |
| `llm-wiki` | `skills/shared/llm-wiki/` | Knowledge management for LLM docs |
| `security-audit` | `skills/shared/security-audit/` | SAST/DAST, OWASP |
| `observability` | `skills/shared/observability/` | JSON logging, OpenTelemetry |
| `technical-writer` | `skills/shared/technical-writer/` | ADRs, Mermaid diagrams, docs |
| `presentation-generator` | `skills/shared/presentation-generator/` | Technical slides, PDFs |

## File Conventions

- **SKILL.md**: The primary skill definition. Contains role description, rules, and workflows.
- **references/**: Supporting documents, standards, and templates referenced by the skill.
- **scripts/**: Automation scripts that the skill may instruct you to run.
- **assets/**: Boilerplate files (e.g., `.gitignore`, `pre-commit-config.yaml`, `justfile`).
- **templates/**: Starter templates for new projects or documentation.

## Agent Rules

1. **Always load the skill** before executing a task that matches the skill's domain.
2. **Enforce the skill's rules** throughout the task. Do not silently drop constraints.
3. **Read references** when a skill points to them. They contain critical standards and templates.
4. **Draft ADRs** for significant architectural decisions using the `technical-writer` skill.
5. **Stay in role** until the task is complete or the user explicitly asks you to switch roles.
6. **Use the `project-owner` skill** when starting new projects or managing backlogs.
