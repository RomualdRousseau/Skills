# GitHub Backlog Workflow

The project backlog is managed exclusively through GitHub Projects and the `gh` CLI. `TODO.md` files are not used when managing the backlog via GitHub.

## Project Setup

- **Project**: GitHub Project board (e.g., project #1 or named board)
- **Repository**: Target repository

## Scope Labels

Every backlog item should have an appropriate scope label (e.g. package or component):

| Label | Use for |
|---|---|
| `<project>-all` | Monorepo-level or cross-cutting stories |
| `<project>-env` | Environment package stories and features |
| `<project>-agents` | Agents package stories and features |

## Creating a New Backlog Item

Create a repo issue, apply the correct label, and add it to the project in one command:

```bash
gh issue create \
  --title "[<scope>] Story: <title>" \
  --body "## Acceptance Criteria\n- [ ] ...\n- [ ] ..." \
  --label "<scope-label>" \
  --project "<project-name>"
```

If the item is already completed, close it immediately:

```bash
gh issue close <issue-number-or-url>
```

## Updating Status

Move items through the board using the GitHub UI or CLI. Do not maintain a local `TODO.md` file.

## Closing Items

When a story is fully implemented and verified:

1. Close the issue with `gh issue close <issue-number-or-url>`.
2. Ensure acceptance criteria in the issue body are checked.
3. Update the README or functional documentation if the change affects user-facing behavior.
