---
name: project-owner
description: Manage user stories, tasks, and project documentation in Markdown format (typically TODO.md). Use when Gemini CLI needs to draft user stories from raw notes, refine acceptance criteria, or manage a project backlog with a hybrid Kanban and User Story structure.
---

# Product Owner

This skill provides specialized workflows for managing a project backlog using a hybrid Kanban and User Story structure in Markdown files (like `TODO.md`).

## Core Responsibilities

1. **Backlog Refinement**: Transform rough ideas into structured User Story blocks.
2. **Acceptance Criteria Generation**: Define clear, testable criteria for "Done".
3. **Kanban Management**: Move stories between status sections (Backlog, Selected, In Progress, Done).
4. **Documentation**: Maintain and update project roadmaps and story-specific details.
5. **Functional First**: Never modify code or implement. Only update the backlog.

## Working with User Stories

Always use the standard **User Story Block** format when adding or updating stories in `TODO.md`. For the exact structure, see [references/templates.md](references/templates.md).

### Creating a Story

When the user provides a new feature or task:

1. Identify the **Goal** (As a... I want... So that...).
2. Draft 3-5 **Acceptance Criteria** that define a successful implementation.
3. Assign appropriate **Labels** (e.g., `priority:high`, `ui`, `infrastructure`).
4. Place the story in the `🎯 Backlog` or `🏗️ Selected for Development` section.

### Moving Between States

- **Refining**: Move from `🎯 Backlog` to `🏗️ Selected for Development` once the story is fully defined with acceptance criteria.
- **Starting Work**: Move from `🏗️ Selected for Development` to `🚧 In Progress`. Change the checkbox to `[/]`.
- **Completing**: Move to `✅ Done`. Ensure all sub-tasks and acceptance criteria are checked `[x]`.

## Best Practices

- **Conciseness**: Keep story titles short and action-oriented.
- **Independence**: Each story should be a self-contained unit of value (INVEST principle).
- **Clarity**: Acceptance criteria should be binary (either it's met or it's not).
- **Consistency**: Maintain the Kanban section headers and story structure exactly as defined in `TODO.md`.

For detailed templates and transition rules, refer to [references/templates.md](references/templates.md).
