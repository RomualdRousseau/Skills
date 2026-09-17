"""Unit tests for agentskills.io skill evaluation toolkit."""

import json
from pathlib import Path

import eval_skill as eval_module
import pytest
from eval_skill import (
    calculate_statistics,
    cmd_benchmark,
    cmd_grade,
    cmd_report,
    cmd_scaffold,
    cmd_validate,
    validate_eval_file,
)


def test_calculate_statistics_empty() -> None:
    """Empty list returns zeroed metrics."""
    stats = calculate_statistics([])
    assert stats["mean"] == 0.0
    assert stats["stddev"] == 0.0


def test_calculate_statistics_single() -> None:
    """Single item returns mean without variance."""
    stats = calculate_statistics([42.0])
    assert stats["mean"] == 42.0
    assert stats["stddev"] == 0.0


def test_calculate_statistics_multiple() -> None:
    """Computes accurate sample mean and standard deviation."""
    stats = calculate_statistics([10.0, 20.0, 30.0])
    assert stats["mean"] == 20.0
    assert stats["stddev"] == 10.0


def test_validate_eval_file_valid(tmp_path: Path) -> None:
    """Valid evals.json returns valid ValidationResult."""
    eval_file = tmp_path / "evals.json"
    _ = eval_file.write_text(
        json.dumps(
            {
                "skill_name": "test-skill",
                "evals": [
                    {
                        "id": 1,
                        "prompt": "Test prompt",
                        "expected_output": "Test output",
                        "assertions": ["Output is correct"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    res = validate_eval_file(eval_file, expected_skill="test-skill")
    assert res.valid is True
    assert res.eval_count == 1
    assert res.assertion_count == 1
    assert not res.errors


def test_validate_eval_file_missing_keys(tmp_path: Path) -> None:
    """Evals file missing required keys reports errors."""
    eval_file = tmp_path / "evals.json"
    eval_file.write_text(json.dumps({}), encoding="utf-8")

    res = validate_eval_file(eval_file, expected_skill="test-skill")
    assert res.valid is False
    assert any("skill_name" in err for err in res.errors)
    assert any("evals" in err for err in res.errors)


def test_cmd_grade_and_benchmark(tmp_path: Path) -> None:
    """Full cycle of grading an eval directory, computing benchmark, and reporting."""
    iteration_dir = tmp_path / "iteration-1"
    eval_1 = iteration_dir / "eval-1"
    with_skill = eval_1 / "with_skill"
    without_skill = eval_1 / "without_skill"

    (with_skill / "outputs").mkdir(parents=True)
    (without_skill / "outputs").mkdir(parents=True)

    assertions = ["File exists", "Content matches standard"]
    (with_skill / "assertions.json").write_text(json.dumps(assertions), encoding="utf-8")
    (without_skill / "assertions.json").write_text(json.dumps(assertions), encoding="utf-8")

    # Add mock timing
    (with_skill / "timing.json").write_text(json.dumps({"duration_ms": 1500, "total_tokens": 500}), encoding="utf-8")
    (without_skill / "timing.json").write_text(json.dumps({"duration_ms": 2500, "total_tokens": 800}), encoding="utf-8")

    # Grade both
    assert cmd_grade(str(with_skill)) == 0
    assert cmd_grade(str(without_skill)) == 0
    assert (with_skill / "grading.json").exists()

    # Benchmark
    assert cmd_benchmark(str(iteration_dir)) == 0
    assert (iteration_dir / "benchmark.json").exists()

    # Report
    assert cmd_report(str(iteration_dir)) == 0


def test_cmd_validate_and_scaffold(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify scaffold and validate commands with temporary skills root."""
    fake_skills = tmp_path / "skills"
    fake_skills.mkdir()
    (fake_skills / "dummy-skill").mkdir()

    monkeypatch.setattr(eval_module, "SKILLS_DIR", fake_skills)

    # Scaffold
    assert cmd_scaffold("dummy-skill") == 0
    eval_file = fake_skills / "dummy-skill" / "evals" / "evals.json"
    assert eval_file.exists()

    # Validate specific
    assert cmd_validate(target_skill="dummy-skill") == 0
    # Validate all
    assert cmd_validate(check_all=True) == 0
