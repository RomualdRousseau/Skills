# ADR 009: Adoption of agentskills.io Evaluation Framework for AI Skills

**Date:** 2026-09-13  
**Status:** Accepted

## Context

The Skills repository defines specialized instructions, domain architectures, and safety constraints for AI agents. However, evaluating and guaranteeing the quality of these skills faced significant challenges:

1. **Lack of Empirical Measurement:** Without quantitative evaluation, it was impossible to prove whether adding a skill produced superior code compared to a baseline model without the skill.
2. **Subjective Quality Assessment:** Evaluating prompt adherence relied largely on ad-hoc human inspection or loose LLM prompts, leading to high variance and unrepeatable results.
3. **Triggering Failures & Rule Erosion:** Updates to skill instructions could inadvertently break natural language triggering or lead to silent omission of critical constraints (e.g., Power of 10 safety rules, typing protocols, seed determinism).
4. **Standardization Need:** The agent ecosystem is standardizing around open specifications. Adopting a proprietary evaluation format would create isolation and vendor lock-in.

The [agentskills.io](https://agentskills.io/skill-creation/evaluating-skills.md) open specification defines an objective, structured standard for skill evaluations using test cases, falsifiable assertions, and comparative uplift benchmarking.

---

## Decision

We adopt the open **agentskills.io** specification as the official skill evaluation framework for this repository:

### 1. File Structure and Schema (`evals/evals.json`)
Evaluation suites reside co-located with their respective skills at `skills/<skill-name>/evals/evals.json`:

```json
{
  "skill_name": "python-developer",
  "evals": [
    {
      "id": 1,
      "prompt": "Implement an iterative graph DFS traversal function with hard loop bounds and slots domain model.",
      "expected_output": "A Python module containing a GraphNode dataclass with __slots__, an iterative DFS implementation with hard loop bounds, and no recursive calls.",
      "files": [],
      "assertions": [
        "The graph node domain model uses @dataclass(slots=True) or explicit __slots__",
        "The DFS algorithm is implemented iteratively using an explicit stack",
        "The algorithm contains zero recursive function calls",
        "The while loop has a hard maximum iteration bound to prevent infinite loops",
        "All functions include strict Python type annotations"
      ]
    }
  ]
}
```

### 2. Verifiable Assertion Design
Assertions must be objective, deterministic, and falsifiable:
- **Structural Invariants:** Specific typing constructs (e.g., `typing.Protocol`, `@dataclass(slots=True)`), file presence, or directory layouts.
- **Behavioral Guarantees:** Zero recursion, bounded loops, seed determinism, explicit error types.
- **Negative Constraints:** Ensuring forbidden dependencies or patterns do not appear (e.g., no framework imports in domain entities, no graphics window initialized in headless RL training).

### 3. Dual-Run Execution & Uplift Benchmarking
To empirically evaluate skills, agents are evaluated across dual execution paths in a dedicated workspace:
- **`without_skill` (Baseline):** Agent executes the prompt using default knowledge without loading the skill.
- **`with_skill`:** Agent executes the prompt with the skill loaded and active.
- **Comparative Uplift (`delta`):** The benchmark computes the differential impact:
  $$\Delta \text{Pass Rate} = \text{Pass Rate}_{\text{with\_skill}} - \text{Pass Rate}_{\text{without\_skill}}$$
  along with execution time differentials and token usage.

### 4. Built-In Evaluation Toolkit (`scripts/eval_skill.py`)
A self-contained Python CLI tool provides complete lifecycle operations without external runtime dependencies:
- **`validate`:** Validates schema syntax, field types, and name consistency.
- **`scaffold`:** Generates starter `evals/evals.json` test suites.
- **`grade`:** Grades output directories against assertions.
- **`benchmark`:** Aggregates run artifacts into statistical summaries (mean, sample standard deviation, deltas).
- **`report`:** Renders Markdown comparison and uplift tables.

### 5. Repository CI & Lint Integration
- `scripts/lint_skills.py` automatically validates all `evals/evals.json` files during `just lint`.
- Repository `justfile` provides developer recipes: `lint-evals`, `scaffold-evals`, `benchmark-evals`, and `report-evals`.

---

## Consequences

### Positive
- **Empirical Rigor:** Provides verifiable proof that skills improve agent performance, accuracy, and constraint adherence.
- **Regression Detection:** Ensures future modifications to skill instructions do not degrade agent behavior or drop mandatory rules.
- **Ecosystem Compatibility:** Fully adheres to the open `agentskills.io` standard, allowing test suites to be used across compatible agent runners.
- **Actionable Feedback:** Grading reports pin-point specific failed assertions, providing clear guidance on how to refine skill prompts.

### Negative
- **Authoring Overhead:** Writing effective, realistic test cases and objective assertions requires upfront engineering effort.
- **Maintenance Cost:** As domain patterns evolve, assertion lists must be maintained alongside skill instructions.

---

## Alternatives Considered

1. **Unconstrained LLM-as-a-Judge:**
   - *Pros:* Easy to set up with open-ended prompts.
   - *Cons:* High evaluation variance, subjective scoring, and non-deterministic results between runs.
2. **Standard Code Unit Tests Only:**
   - *Pros:* Deterministic and fast.
   - *Cons:* Tests only the final generated code artifact in a fixed setup; fails to test the agent's interactive prompting adherence, triggering fidelity, or architectural decision-making.
3. **Manual Human Code Review:**
   - *Pros:* High nuance.
   - *Cons:* Does not scale across 20+ skills, cannot be automated in CI, and lacks quantitative tracking over time.
