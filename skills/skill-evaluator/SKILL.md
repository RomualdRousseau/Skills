---
name: skill-evaluator
description: Standardized workflow for validating, scaffolding, executing dual-run A/B benchmarks, grading assertions, and reporting uplift for AI skills conforming to agentskills.io.
tags:
  - evaluation
  - agentskills
  - benchmark
  - testing
depends_on: []
---

# Skill Evaluator

This skill provides a standardized, empirical evaluation framework for AI agent skills conforming to the open [agentskills.io specification](https://agentskills.io/skill-creation/evaluating-skills.md).

## 1. Evaluation Lifecycle Overview

Evaluating an AI skill follows a strict 5-step lifecycle:

1. **Validation**: Validate `evals/evals.json` against the agentskills.io schema using `just lint-evals`.
2. **Isolation**: Prepare isolated working directories under `/tmp/opencode/` to prevent repository context (e.g., `AGENTS.md` or active skill files) from leaking into baseline runs.
3. **Dual-Run Execution (A/B Benchmark)**: Run each evaluation test case across two subagent execution paths:
   - **`with_skill`**: Subagent explicitly reads and enforces `SKILL.md` and reference documents.
   - **`without_skill`**: Subagent receives identical prompt with generic professional guidance only.
4. **Honest Assertion Grading**: Inspect generated outputs and evaluate each assertion objectively (recording PASS/FAIL and explicit code evidence in `grading.json`).
5. **Aggregation & Reporting**: Aggregate metrics into `benchmark.json` (`just benchmark-evals <dir>`), render the Markdown uplift report (`just report-evals <dir>`), and record qualitative feedback in `feedback.json`.

## 2. Workspace & Artifact Conventions

All evaluation run artifacts reside under `evals-workspace/iteration-<N>/`:

```
evals-workspace/iteration-1/
├── eval-1/
│   ├── with_skill/
│   │   ├── outputs/         # Generated code artifacts
│   │   ├── assertions.json  # Case assertions list
│   │   ├── grading.json     # Honest pass/fail results + code evidence
│   │   └── timing.json      # Duration ms & token estimates
│   └── without_skill/
│       ├── outputs/
│       ├── assertions.json
│       ├── grading.json
│       └── timing.json
├── benchmark.json           # Aggregated statistics (means, stddev, uplift deltas)
└── feedback.json            # Qualitative notes, caveats, & recommendations
```

## 3. Reference Standards

- **[evaluation-protocol.md](references/evaluation-protocol.md)**: Detailed step-by-step workflow, CLI commands, and grading guidelines.
- **[subagent-prompts.md](references/subagent-prompts.md)**: Standardized subagent prompt templates for `with_skill` and `without_skill` executions.

## Project Interaction

- **Trigger**: "Evaluate the [skill-name] skill"
- **Trigger**: "Run an A/B benchmark for [skill-name]"
- **Trigger**: "Scaffold an evaluation suite for [skill-name]"
- **Trigger**: "Grade evaluation outputs for [skill-name]"
- **Trigger**: "Generate a skill uplift report for [iteration-dir]"
