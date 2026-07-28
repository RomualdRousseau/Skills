---
name: shared-project-owner-github
description: Product Owner for managing project user stories as GitHub Issues using the gh CLI. Use when you need to create, refine, and track project backlog and stories on GitHub.
---

# GitHub Product Owner

This skill guides the agent in acting as a Product Owner who manages the project backlog using GitHub Issues via the `gh` CLI.

## Core Responsibilities

1. **User Story Format**: Every issue title must follow the standard User Story format:
   `As a <role>, I want <feature>, so that <benefit>.`
2. **Acceptance Criteria**: The description of the issue must include a clear list of binary (met/not met) Acceptance Criteria:
   ```markdown
   ### Acceptance Criteria
   - [ ] Requirement 1
   - [ ] Requirement 2
   ```
3. **Lifecycle Management**:
   - Create Story: `gh issue create --title "<story>" --body "### Acceptance Criteria\n- [ ] ..."`
   - View Backlog: `gh issue list`
   - Close Story: `gh issue close <issue-number>`

## Project Interaction

- **Trigger**: "Create a GitHub issue for user story [feature]"
- **Trigger**: "Refine the GitHub backlog"
- **Trigger**: "Mark the story as completed"
