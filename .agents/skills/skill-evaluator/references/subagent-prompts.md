# Standardized Subagent Prompt Templates

This document provides templates for launching subagent benchmark runs during skill evaluations.

---

## 1. `with_skill` Subagent Prompt Template

Use this prompt template when launching subagents for the **`with_skill`** execution path:

```markdown
You are an evaluation agent. This is an execution task; WRITE CODE.

TASK: <EVAL_PROMPT_FROM_EVALS_JSON>

FIRST — Load and ADOPT the "<SKILL_NAME>" skill. Read these files in order and treat them as mandatory, enforced constraints for the entire task:
1. /home/romuald/Projects/Perso/Skills/skills/<SKILL_NAME>/SKILL.md
2. <ADDITIONAL_REFERENCE_FILES_IF_ANY>

You MUST actively enforce the skill's rules and conventions.

WRITE the solution into directory: /tmp/opencode/eval-<SKILL_NAME>/eval-<CASE_ID>/with_skill
- Create the necessary Python modules and test files matching the prompt requirements.

Do NOT read any other repository files. Do NOT create GitHub issues. Do NOT violate skill rules.

In your final message, report ONLY: the list of files you wrote (absolute paths), and a one-line summary of which skill constraints you applied.
```

---

## 2. `without_skill` (Baseline) Subagent Prompt Template

Use this prompt template when launching subagents for the **`without_skill`** execution path:

```markdown
You are an evaluation agent. This is an execution task; WRITE CODE.

TASK: <EVAL_PROMPT_FROM_EVALS_JSON>

Use your default professional Python knowledge and judgment. No external skill, ruleset, or constraint file has been provided to you.

WRITE the solution into directory: /tmp/opencode/eval-<SKILL_NAME>/eval-<CASE_ID>/without_skill
- Create the necessary Python modules and test files matching the prompt requirements.

Do NOT read any files outside your working directory. Do NOT create GitHub issues.

In your final message, report ONLY: the list of files you wrote (absolute paths), and a one-line summary of the design choices you made.
```

---

## 3. Best Practices for Subagent Execution

- **Directory Isolation**: Always run subagents in `/tmp/opencode/eval-<SKILL_NAME>/...` to prevent baseline agents from discovering repository `AGENTS.md` or active skill files.
- **Parallel Execution**: Issue both `with_skill` and `without_skill` subagent calls in parallel within a single message to maximize throughput.
- **No Git Operations**: Instruct subagents not to commit or interact with GitHub issues.
