# Skills Evaluation & Benchmark Report

This document compiles empirical A/B benchmark evaluation results for skills in this repository, conforming to the open **[agentskills.io specification](https://agentskills.io/skill-creation/evaluating-skills.md)**.

---

## 1. Executive Summary

Empirical dual-run evaluations compare agent performance **with** the skill loaded against an unconstrained **baseline** (without the skill). Across all evaluated skills, activating the skill yields a **100.0% pass rate** on falsifiable architectural and safety assertions, demonstrating significant performance uplift over baselines.

| Skill | Baseline Pass Rate | With Skill Pass Rate | Pass Rate Uplift ($\Delta$) | Time Delta | Token Delta | Evaluation Status |
|---|---|---|---|---|---|---|
| **`python-developer`** | 77.5% | **100.0%** | **+22.5%** | +115.7s | +2,314 | Verified (2 cases / 9 assertions) |
| **`python-hexagonal`** | 65.0% | **100.0%** | **+35.0%** | +34.0s | +679 | Verified (2 cases / 9 assertions) |
| **`data-engineer`** | 65.0% | **100.0%** | **+35.0%** | +36.5s | +730 | Verified (2 cases / 9 assertions) |
| **`product-owner`** | 62.5% | **100.0%** | **+37.5%** | **-55.1s** | **-1,101** | Verified (2 cases / 8 assertions) |

**Overall Mean Assertion Uplift:** **+32.5% Compliance** across all evaluated skills.

---

## 2. Skill Evaluation Summaries

### 🐍 `python-developer`
- **Baseline Pass Rate:** 77.5%
- **With Skill Pass Rate:** 100.0%
- **Pass Rate Uplift ($\Delta$):** **+22.5%**
- **Test Suite:** 2 test cases (9 assertions total)
- **Evaluation Summary:**
  - **What the Skill Added:** Enforced Power of 10 safety rules, specifically hard loop bounds (`MAX_ITERATIONS` + fail-closed `TraversalLimitError`), `TypeGuard` boundary validation, `typing.Protocol` decoupling, `slots=True` on domain models, and Hypothesis property-based testing.
  - **Baseline Omissions:** Baseline models produced reasonable code but routinely omitted hard loop bounds (`while stack:` with no max iteration guard) and used raw `isinstance`/`typing.Any` checks instead of runtime `TypeGuard` boundary validation.

---

### 🏛️ `python-hexagonal`
- **Baseline Pass Rate:** 65.0%
- **With Skill Pass Rate:** 100.0%
- **Pass Rate Uplift ($\Delta$):** **+35.0%**
- **Test Suite:** 2 test cases (9 assertions total)
- **Evaluation Summary:**
  - **What the Skill Added:** Enforced `@dataclass(slots=True)` / `__slots__` memory discipline on domain entities, `typing.Protocol` secondary port definitions, pure domain state transition methods on entities (e.g. `pay()`, `fulfill()`, `cancel()` enforcing invariants), zero framework imports in domain entities, and strict constructor dependency injection in application services.
  - **Baseline Omissions:** Baseline models omitted `slots=True` memory discipline, used classical `abc.ABC` inheritance instead of `typing.Protocol` ports, and created passive/anemic domain models where state transitions were directly mutated by application services.

---

### ⚡ `data-engineer`
- **Baseline Pass Rate:** 65.0%
- **With Skill Pass Rate:** 100.0%
- **Pass Rate Uplift ($\Delta$):** **+35.0%**
- **Test Suite:** 2 test cases (9 assertions total)
- **Evaluation Summary:**
  - **What the Skill Added:** Enforced Medallion Silver transformation standards using Polars `LazyFrame` lazy execution before collection, `DataWriterPort` using `typing.Protocol`, Pydantic models for boundary schema validation with fail-closed quarantine routing, and constructor dependency injection into application stages.
  - **Baseline Omissions:** Baseline models fell back to eager Polars `DataFrame` execution (missing lazy frames), used classical `abc.ABC` inheritance instead of `typing.Protocol` ports, and omitted application stage classes for dependency injection.

---

### 📋 `product-owner`
- **Baseline Pass Rate:** 62.5%
- **With Skill Pass Rate:** 100.0%
- **Pass Rate Uplift ($\Delta$):** **+37.5%**
- **Test Suite:** 2 test cases (8 assertions total)
- **Efficiency Impact:** **68.3% token reduction** (-1,101 tokens) and **55.1 seconds faster** execution time.
- **Evaluation Summary:**
  - **What the Skill Added:** Enforced binary testable acceptance criteria as markdown checkbox lists (`- [ ]`), strict adherence to user-facing outcomes without prescribing technical implementation details (preventing premature technical architecture specification in user stories), and explicit categorization into backlog lifecycle stages (`Selected for Development`, `Backlog`, `Icebox`).
  - **Baseline Omissions:** Baseline models suffered from scope bloat (over-prescribing technical implementation details like AES-256 encryption standards and database password hashing) and omitted backlog lifecycle stage categorizations.

---

## 3. Benchmark Methodology & Workflow

Evaluations are executed using the repository's `skill-evaluator` skill and CLI tooling:

```bash
# 1. Validate evals suite schema
just lint-evals

# 2. Run dual-execution A/B benchmark in isolated workspace (/tmp/opencode/)
# 3. Grade assertions objectively against generated artifacts (grading.json)

# 4. Aggregate benchmark statistics and render uplift report
just benchmark-evals evals-workspace/<iteration-dir>
just report-evals evals-workspace/<iteration-dir>
```

- **Evaluation Specification:** `scripts/eval_skill.py` conforming to [agentskills.io](https://agentskills.io/skill-creation/evaluating-skills.md).
- **Workspace Isolation:** All `without_skill` baseline runs are executed in isolated `/tmp/opencode/` directories to prevent repository context leakage (`AGENTS.md` or active skill files).
