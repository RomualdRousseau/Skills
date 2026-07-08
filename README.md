# Skills Repository

A high-integrity framework for building specialized AI environments and robust Python applications using **Gemini CLI**.

## 🚀 Getting Started

This repository contains a suite of **Specialized Skills** designed to guide Gemini through complex engineering, research, and design tasks. These skills enforce the "Power of 10" safety rules, hexagonal architecture, and rigorous Reinforcement Learning (RL) practices.

### 1. Activating a Skill

To use these specialized instructions, call `/` with the name of the skill you need:

```bash
/ai-architect
```

### 2. Following the Workflow

All development follows a strict **Research -> Strategy -> Execution** lifecycle:

1.  **Research:** Gemini maps the codebase and validates all assumptions.
2.  **Strategy:** Gemini proposes a grounded plan based on the research.
3.  **Execution:** Gemini implements the plan using the iterative **Plan -> Act -> Validate** cycle.

### 3. Installing & Managing Skills

You can install, browse, and manage Agent Skills using the **Agent Skills** standard CLI tool (`npx skills`), the native `gemini skills` CLI, or interactive slash commands during a session.

#### Using `npx skills` (Interoperable CLI)
The `npx skills` tool allows you to browse, search, and install skills from remote registries directly:

- **Browse and list available remote skills:**
  ```bash
  npx skills add romualdrousseau/skills --list
  ```
- **Install a specific skill from a registry:**
  ```bash
  npx skills add romualdrousseau/skills --skill gemini-live-api-dev
  ```
- **Install a skill globally:**
  ```bash
  npx skills add romualdrousseau/skills --skill gemini-live-api-dev --global
  ```

#### Native CLI Management (`gemini skills`)
Alternatively, you can manage skills using the native Gemini CLI from your terminal:

- **Install a skill from a Git repository or local package:**
  ```bash
  # Install globally (default)
  gemini skills install https://github.com/user/my-awesome-skill

  # Install in local workspace
  gemini skills install https://github.com/user/my-awesome-skill --scope workspace
  ```
- **Link a local skill during development:**
  ```bash
  gemini skills link ./path/to/my-skill
  ```
- **List installed skills:**
  ```bash
  gemini skills list
  ```
- **Uninstall an installed/linked skill:**
  ```bash
  gemini skills uninstall my-skill
  ```

#### In-Session Management (Slash Commands)
Inside an active interactive Gemini CLI session, you can run:
- `/skills list` — Show all discovered, active skills.
- `/skills reload` — Reload skills from disk immediately.
- `/skills enable <name>` / `/skills disable <name>` — Toggle a specific skill.

---

## 🛠️ Available Skills

### Core Python Development (`skills/python-app/`)

- **`developer`**: The "Source of Truth" for high-integrity Python. Enforces the **Power of 10** rules, Hexagonal Architecture, and Light CQRS.
- **`project-owner-todo`**: Manages the `TODO.md` backlog, user stories, and acceptance criteria in Markdown format with a hybrid Kanban structure.
- **`project-owner-glab`**: Manages user stories, tasks, and project backlog using GitLab Issues and the `glab` CLI.
- **`devops`**: Handles GCP infrastructure via Terraform and GitLab CI/CD (Workload Identity Federation).

### Gymnasium & AI Environments (`skills/gymnasium-env/`)

- **`developer`**: Builds high-performance, visually-debuggable RL environments using **Raylib** and the **Scene Pattern**.
- **`designer`**: Environment Designer & Project Owner. Focuses on "The Fun Factor", playable pedagogy, and backlog management (User Stories).
- **`data-scientist`**: RL Environment Architect & Data Scientist. Manages MDP formulation (states, actions, rewards) and the full research lifecycle.

### Data Engineering (`skills/data-pipeline/`)

- **`data-engineer`**: Builds high-integrity data pipelines using the **Medallion Hexagonal Architecture**, **Polars**, and **Pydantic**.

### Research & Variant Analysis (`skills/research/`)

- **`data-scientist`**: Fast-tracked data exploration and ML using **uv** and **Jupyter Notebooks**.
- **`variant-analysis`**: Automated genomic variant analysis (VEP) and clinical assessment using the Variant Analysis Multi-Agent System.

### Shared Engineering Standards (`skills/shared/`)

- **`ai-architect`**: Best practices for RAG patterns, prompt versioning, and LLM evaluation (Ragas/LangSmith).
- **`llm-wiki`**: Knowledge management and preprocessing for LLM-ready documentation.
- **`security-audit`**: Automated SAST/DAST integration and OWASP-aligned coding.
- **`observability`**: Standards for structured JSON logging and OpenTelemetry (OTel) tracing.
- **`technical-writer`**: Mandates **Architecture Decision Records (ADR)** and **Mermaid.js** diagrams.
- **`presentation-generator`**: Automated generation of technical slides and PDF documentation.
- **`html-prez`**: Generates high-fidelity, interactive HTML5/Tailwind CSS presentation slides with multi-format widescreen compilation (PDF, PPTX, PNG). Note: **PPTX exports are pixel-perfect but not editable** (compiled from static slide image screenshots).
- **`svg-prez`**: High-fidelity, direct vector presentation slide generation with clean SVG coordinates and rapid widescreen compilations (SVG, PPTX, PDF, PNG). Note: **PPTX exports are native and fully editable but not pixel-perfect** (compiled directly from vector coordinates).

---

## 🏗️ Architectural Foundations

### The "Power of 10" Safety Rules

All developers (both human and AI) must adhere to these rules:

1.  **No Recursion**: Use iterative stacks.
2.  **Hard Loop Bounds**: Every `while` loop must have a `MAX_ITERATIONS`.
3.  **Memory Discipline**: Use `__slots__` for domain models.
4.  **Boundary Validation**: Use `TypeGuards` at entry points.
5.  **Pure Functions**: Business logic must be side-effect free.
6.  **Dependency Injection**: Pass, don't construct, collaborators.
7.  **No Magic**: Forbidden use of `eval()`, `exec()`, or `getattr()`.
8.  **Protocol Interfaces**: Decouple layers with `typing.Protocol`.
9.  **Fail-Closed**: Logic must default to "abort" on ambiguity.
10. **Test the Invariants**: Use property-based testing (Hypothesis).

### ADR Process

Significant technical decisions are recorded in `docs/adr/`. When Gemini proposes a major change, it will:

1.  Draft a new ADR using the `adr-template.md`.
2.  Seek approval before proceeding.
3.  Store the decision for long-term project context.

---

## 🚦 Interaction Triggers

Each skill includes a **Project Interaction** section that defines specific natural language triggers. These triggers help Gemini CLI identify the correct workflow. Examples include:

- **"Start a new project"**: Activates `project-owner` or `designer` (for AI envs), and `devops` to scaffold the environment.
- **"Implement [feature]"**: Activates `developer` and `technical-writer` to build and document the change.
- **"Optimize the agent"**: Activates `data-scientist` to set up hyperparameter sweeps and evaluation reports.
- **"Audit the codebase"**: Activates `security-audit` and `ai-architect` to identify vulnerabilities and RAG bottlenecks.

---

## 🤝 Credits

- **`llm-wiki`**: Credits to [Andrej Karpathy's gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki).
- **`presentation-generator`**: Credits to [Kévin François-Bouaou, PhD](https://fr.linkedin.com/in/kevin-fran%C3%A7ois-bouaou-phd).

---

## 📄 License
