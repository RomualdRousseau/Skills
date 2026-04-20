---
name: technical-writer
description: Focuses on maintaining high-quality Architecture Decision Records (ADRs), automated documentation, and code readability.
---

# Technical Writer

This skill ensures that architectural decisions are preserved, systems are well-documented, and context is shared asynchronously.

## 1. Architecture Decision Records (ADR)
- **Documenting Decisions:** Any significant architectural choice, library addition, or pattern change must be recorded as an ADR.
- **Location:** Store ADRs in `docs/adr/` or `references/adr/`.
- **Template:** Use the standard ADR template located in `references/adr-template.md`.

## 2. Documentation as Code
- **Diagrams:** Use Mermaid.js within Markdown files for sequence diagrams, flowcharts, and architecture diagrams. They are version-controllable and render natively in Git platforms.
- **API Docs:** Use automated tools (Swagger/OpenAPI, ReDoc) to generate API documentation from code. Avoid maintaining external wikis for API specs.

## 3. Code Comments & Readability
- **The "Why", Not the "What":** Code explains *what* is happening. Comments explain *why* it is happening (e.g., business rules, hacky workarounds for bugs).
- **Docstrings:** Use consistent docstring formats (e.g., Google or Sphinx) for public modules, classes, and functions.

## Project Interaction

- **Trigger**: "Draft an ADR for [decision/change]"
- **Trigger**: "Create a Mermaid diagram for [architecture/workflow]"
- **Trigger**: "Refine the docstrings for [module]"
- **Trigger**: "Generate the API documentation for [service]"
- **Trigger**: "Update the project technical documentation with [new context]"

