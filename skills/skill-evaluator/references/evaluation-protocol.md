# Skill Evaluation Protocol

This reference describes the step-by-step procedure for executing an empirical skill evaluation adhering to the agentskills.io standard.

---

## 1. Schema Validation

Before running any benchmark, verify that `skills/<skill-name>/evals/evals.json` exists and is valid:

```bash
uv run python scripts/eval_skill.py validate <skill-name>
# Or validate all skills:
just lint-evals
```

If `evals.json` is missing, scaffold a starter suite:

```bash
just scaffold-evals <skill-name>
```

---

## 2. Workspace Setup

Create the iteration workspace structure under `evals-workspace/iteration-1/`:

```bash
mkdir -p evals-workspace/iteration-1/eval-1/with_skill/outputs \
         evals-workspace/iteration-1/eval-1/without_skill/outputs \
         evals-workspace/iteration-1/eval-2/with_skill/outputs \
         evals-workspace/iteration-1/eval-2/without_skill/outputs
```

Create temporary execution directories in `/tmp/opencode/` for isolated subagent execution:

```bash
mkdir -p /tmp/opencode/eval-<skill-name>/eval-1/with_skill \
         /tmp/opencode/eval-<skill-name>/eval-1/without_skill \
         /tmp/opencode/eval-<skill-name>/eval-2/with_skill \
         /tmp/opencode/eval-<skill-name>/eval-2/without_skill
```

---

## 3. Dual-Run Subagent Benchmark Execution

For each test case in `evals.json`:

1. Launch two subagents in parallel using the `Task` tool (`subagent_type: general`):
   - **`with_skill`**: Prompts the subagent to read and enforce `skills/<skill-name>/SKILL.md` and reference files before implementing the solution in `/tmp/opencode/.../with_skill/`.
   - **`without_skill`**: Prompts the subagent with the identical prompt and generic professional guidance in `/tmp/opencode/.../without_skill/`.
2. Copy generated `.py` / output files from `/tmp/opencode/` to `evals-workspace/iteration-1/eval-<N>/<variant>/outputs/`.

See [subagent-prompts.md](subagent-prompts.md) for standard prompt templates.

---

## 4. Honest Assertion Grading

Read all generated output files. Inspect each file against the test case assertions.

For each variant (`with_skill` and `without_skill`):

1. Write `assertions.json`: list of assertion strings for that test case.
2. Write `grading.json`:

```json
{
  "assertion_results": [
    {
      "text": "The domain entity defines __slots__ or uses @dataclass(slots=True)",
      "passed": true,
      "evidence": "@dataclass(slots=True, eq=False) on GraphNode (graph_traversal.py:34)"
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 0,
    "total": 1,
    "pass_rate": 1.0
  }
}
```

3. Write `timing.json`:

```json
{
  "duration_ms": 150000,
  "total_tokens": 3000
}
```

---

## 5. Benchmark Aggregation & Uplift Reporting

1. Run benchmark aggregation:
   ```bash
   just benchmark-evals evals-workspace/iteration-1
   ```
2. Render Markdown uplift table:
   ```bash
   just report-evals evals-workspace/iteration-1
   ```
3. Record qualitative notes in `evals-workspace/iteration-1/feedback.json`:

```json
{
  "overall": "High-level summary of evaluation results.",
  "what_skill_added": "Key architectural and safety patterns introduced by the skill.",
  "baseline_leaks": "Omissions or anti-patterns observed in the baseline runs.",
  "timing_tokens_limitation": "Note on timing and token measurement methodology.",
  "recommendations": [
    "Actionable recommendations for skill prompt improvements or tooling."
  ]
}
```
