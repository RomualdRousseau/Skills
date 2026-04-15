# TODO.md Specification

In a monorepo, `TODO.md` files are scoped to their respective packages or the root. The file must always maintain three distinct sections to track the project's state.

## Required Sections

### 1. # [Scope] Backlog
Contains all ideas, feature requests, and future user stories for the specific scope (e.g., `# Monorepo Backlog`, `# Agents Backlog`). These are not yet prioritized for development.
- [ ] Story: As a player, I want...
- [ ] Feature: Character Customization

### 2. # To Be Developed (In Progress)
Contains the current sprint's or task's active user stories and their sub-tasks.
- [ ] Story: Implement basic movement
  - [ ] Task: Handle WASD input
  - [ ] Task: Apply velocity to player state

### 3. # Done
Contains all completed stories and tasks. Move items here only when all acceptance criteria are met.
- [x] Task: Initialize project structure
- [x] Story: Setup Raylib window

## Monorepo Structure
- **Root TODO.md**: Tracks high-level architectural changes, cross-cutting features, and multi-package stories.
- **Package TODO.md**: Tracks feature-specific stories and tasks for a specific module (e.g., `Environment/TODO.md`).
