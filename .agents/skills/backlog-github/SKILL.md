---
name: backlog-github
description: Manage project backlog, user stories, and issue tracking using GitHub Issues and Projects via the gh CLI.
tags:
  - github
  - cli
  - issues
  - projects
  - backlog
  - tracking
depends_on:
  - product-owner
---

# Backlog GitHub

This skill provides specialized workflows for managing an agile project backlog and user stories through **GitHub Issues** and **GitHub Projects** using the `gh` command-line tool. Extending `product-owner`, it enables automated issue creation, backlog querying, and status updates directly from the terminal.

## 1. Creating User Stories as Issues

Use `gh issue create` to submit stories refined via `product-owner`:

```bash
gh issue create \
  --title "Story: [Concise Title]" \
  --body "### Goal
As a [role], I want [action], so that [value].

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]" \
  --label "enhancement" \
  --project "<project-name-or-number>"
```

Refer to [github-backlog.md](references/github-backlog.md) for full project board workflows and label strategies.

## 2. Inspecting and Filtering the Backlog

Use standard `gh` commands to inspect project items and milestones:

```bash
# List all backlog items in a project
gh project item-list <project-number> --owner @me

# List open issues with a specific label
gh issue list --label "<scope-label>"

# View details of a specific issue
gh issue view <issue-id>
```

## 3. Advancing and Closing Stories

- **Update Criteria**: Update issue description as ACs are completed (`gh issue edit <id> --body "..."`).
- **Close on Verification**: Once all acceptance criteria pass and tests are verified, close the issue:
  ```bash
  gh issue close <issue-id> --comment "Verified against all acceptance criteria."
  ```

## Project Interaction

- **Trigger**: "Create a GitHub issue for [feature]"
- **Trigger**: "List open issues in the GitHub project backlog"
- **Trigger**: "Close GitHub issue [number] after verifying criteria"
- **Trigger**: "Filter GitHub issues by label [label]"
