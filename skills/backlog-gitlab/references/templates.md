# Product Owner Templates (GitLab)

## 📝 glab Issue Creation Command

Use this template to create a new user story as a GitLab issue.

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

## 📋 Common Labels

Use these labels to categorize and prioritize issues:

- **Priority**: `priority:high`, `priority:medium`, `priority:low`
- **Domain**: `core`, `infrastructure`, `ui`, `analysis`, `reporting`, `prompts`
- **Quality**: `qa`, `devops`, `performance`
- **Status**: `unrefined`, `blocked`

## 🔄 Issue Lifecycle

- **Create**: Use the template above to add to the backlog.
- **Start**: Optionally assign yourself or update labels.
- **Update**: Use `glab issue update <id> --description "..."` to refine ACs.
- **Close**: Use `glab issue close <id>` when work is verified against ACs.
