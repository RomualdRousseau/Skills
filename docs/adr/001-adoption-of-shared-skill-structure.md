# ADR 001: Adoption of Shared Skill Structure

**Date:** 2026-04-15
**Status:** Accepted

## Context
As the AIInnoLab ecosystem grows, we are introducing multiple specialized skill sets (e.g., `python-app`, `gymnasium-env`). Many engineering practices—such as security auditing, observability, AI/LLM architecture, and technical writing—are universal and apply regardless of the specific application type or language.

Before this decision, there was a risk of duplicating these core standards within each project-specific directory, leading to inconsistent guidance and maintenance overhead.

## Decision
We will introduce a `skills/shared/` directory to house all cross-cutting, high-integrity engineering and architectural standards. Project-specific skills (e.g., `skills/python-app/developer`) should reference these shared skills rather than redefining universal practices.

We will also adopt a formal Architecture Decision Record (ADR) process to document significant technical choices, ensuring project context is preserved over time.

## Consequences
- **Positive:**
  - **Consistency:** All projects (current and future) follow the same high-integrity security and observability standards.
  - **Reduced Duplication:** We avoid maintaining multiple versions of the same core principles (e.g., OWASP, RAG patterns).
  - **Knowledge Preservation:** The ADR process ensures that "why" decisions were made is as clear as "how" they were implemented.
- **Negative:**
  - **Structure Complexity:** Adds one additional layer to the `skills/` directory hierarchy.
  - **Cross-Referencing:** Requires agents and developers to check both shared and project-specific skills.

## Alternatives Considered
- **Siloed Skills:** Keeping all skills inside project-specific folders (e.g., `skills/python-app/security`). This was rejected due to high maintenance overhead and the risk of standards drifting apart between projects.
- **Root-level Skills:** Placing shared skills directly in the root `skills/` folder. This was rejected to keep the top-level directory clean and distinguish between "roles" (Developer, PO) and "specializations" (AI, Security).
