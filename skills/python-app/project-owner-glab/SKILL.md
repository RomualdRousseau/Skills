---
name: project-owner-glab
description: Manage user stories, tasks, and project backlog using GitLab Issues and the glab CLI. Use when Gemini CLI needs to draft user stories, refine acceptance criteria, or manage the project roadmap.
---

# Product Owner

This skill provides specialized workflows for managing a project backlog using GitLab Issues via the `glab` CLI.

## Core Responsibilities

1. **Backlog Refinement**: Transform rough ideas into structured GitLab Issues.
2. **Acceptance Criteria Generation**: Define clear, testable criteria as Markdown checklists within issue descriptions.
3. **Issue Management**: Create, list, view, and close issues to track progress.
4. **Documentation**: Maintain and update project documentation to reflect completed work.

## Working with User Stories

Always use the standard **User Story** format when creating or updating issues.

### Creating an Issue

When the user provides a new feature or task, use `glab issue create`:

1. **Title**: Action-oriented and concise (e.g., "Story: Implement XYZ").
2. **Description**:
   - Start with the **Goal** (As a... I want... So that...).
   - Include a **### Acceptance Criteria** section with Markdown checkboxes (`- [ ]`).
3. **Labels**: Assign appropriate labels using `--label` (e.g., `priority:high`, `ui`, `infrastructure`).

### Managing Workflow

- **Refining**: Use `glab issue list` and `glab issue view <id>` to review and refine stories.
- **Tracking**: Check off acceptance criteria in GitLab as they are completed.
- **Completing**: Use `glab issue close <id>` once all criteria are met and verified.

## Best Practices

- **Conciseness**: Keep story titles short and action-oriented.
- **Independence**: Each story should be a self-contained unit of value (INVEST principle).
- **Clarity**: Acceptance criteria should be binary (either it's met or it's not).
- **Tooling**: Prefer `glab` CLI for all backlog interactions to ensure the remote source of truth is updated.
