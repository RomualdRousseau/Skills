---
name: backlog-gitlab
description: Manage project backlog, user stories, and issue tracking using GitLab Issues via the glab CLI.
tags:
  - gitlab
  - cli
  - issues
  - backlog
  - tracking
depends_on:
  - product-owner
---

# Backlog GitLab

This skill provides specialized workflows for managing an agile project backlog and user stories through **GitLab Issues** using the `glab` command-line tool. Extending `product-owner`, it enables automated issue creation, milestone tracking, and status transitions directly from the terminal.

## 1. Creating User Stories as GitLab Issues

Use `glab issue create` to submit stories refined via `product-owner`:

```bash
glab issue create \
  --title "Story: [Concise Title]" \
  --description "**Goal:** As a [role], I want [action], so that [value].

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]" \
  --label "priority:medium,unrefined"
```

Refer to [templates.md](references/templates.md) for issue creation templates, label strategies, and lifecycle commands.

## 2. Inspecting and Filtering the Backlog

Use standard `glab` commands to query project issues:

```bash
# List all open issues
glab issue list

# Filter issues by label
glab issue list --label "priority:high"

# View details of a specific issue
glab issue view <issue-id>
```

## 3. Advancing and Closing Stories

- **Refining**: Use `glab issue update <id> --description "..."` to refine acceptance criteria.
- **Closing**: Use `glab issue close <id>` when work is verified against all acceptance criteria.

## Project Interaction

- **Trigger**: "Create a GitLab issue for [feature]"
- **Trigger**: "List open issues in the GitLab project backlog"
- **Trigger**: "Close GitLab issue [number] after verifying criteria"
- **Trigger**: "Refine acceptance criteria on GitLab issue [id]"
