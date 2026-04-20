# AIInnoLab Skills Repository

A high-integrity framework for building specialized AI environments and robust Python applications using **Gemini CLI**.

## 🚀 Getting Started

This repository contains a suite of **Specialized Skills** designed to guide Gemini through complex engineering, research, and design tasks. These skills enforce the "Power of 10" safety rules, hexagonal architecture, and rigorous Reinforcement Learning (RL) practices.

### 1. Activating a Skill
To use these specialized instructions, call the `activate_skill` tool with the name of the skill you need:

```bash
/activate_skill ai-architect
```

### 2. Following the Workflow
All development follows a strict **Research -> Strategy -> Execution** lifecycle:
1.  **Research:** Gemini maps the codebase and validates all assumptions.
2.  **Strategy:** Gemini proposes a grounded plan based on the research.
3.  **Execution:** Gemini implements the plan using the iterative **Plan -> Act -> Validate** cycle.

---

## 🛠️ Available Skills

### Core Python Development (`skills/python-app/`)
- **`developer`**: The "Source of Truth" for high-integrity Python. Enforces the **Power of 10** rules, Hexagonal Architecture, and Light CQRS.
- **`project-owner`**: Manages the `TODO.md` backlog, user stories, and acceptance criteria.
- **`devops`**: Handles GCP infrastructure via Terraform and GitLab CI/CD (Workload Identity Federation).

### Gymnasium & AI Environments (`skills/gymnasium-env/`)
- **`developer`**: Builds high-performance, visually-debuggable RL environments using **Raylib** and the **Scene Pattern**.
- **`designer`**: Environment Designer & Project Owner. Focuses on "The Fun Factor", playable pedagogy, and backlog management (User Stories).
- **`data-scientist`**: RL Environment Architect & Data Scientist. Manages MDP formulation (states, actions, rewards) and the full research lifecycle.

### Shared Engineering Standards (`skills/shared/`)
- **`ai-architect`**: Best practices for RAG patterns, prompt versioning, and LLM evaluation (Ragas/LangSmith).
- **`security-audit`**: Automated SAST/DAST integration and OWASP-aligned coding.
- **`observability`**: Standards for structured JSON logging and OpenTelemetry (OTel) tracing.
- **`technical-writer`**: Mandates **Architecture Decision Records (ADR)** and **Mermaid.js** diagrams.

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

- **"Start a new project"**: Activates `project-owner` and `devops` to scaffold the environment.
- **"Implement [feature]"**: Activates `developer` and `technical-writer` to build and document the change.
- **"Optimize the agent"**: Activates `data-scientist` to set up hyperparameter sweeps and evaluation reports.
- **"Audit the codebase"**: Activates `security-audit` and `ai-architect` to identify vulnerabilities and RAG bottlenecks.

---

## 📄 License
This repository is private to the **AIInnoLab** ecosystem.
