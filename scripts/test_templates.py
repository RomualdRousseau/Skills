#!/usr/bin/env python3
"""Automated integration test runner for all project templates.

Tests each template by:
1. Instantiating it via Copier in an isolated temporary directory.
2. Validating required files (AGENTS.md, pyproject.toml, justfile, tests/).
3. Running `uv run --no-env-file pytest`.
4. Running `uvx --no-env-file ruff check .` and `uvx --no-env-file ruff format --check .`.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

TEMPLATES = [
    "python-app",
    "python-game",
    "data-pipeline",
    "gymnasium-env",
]

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_command(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    """Execute command in target directory and return returncode, stdout, stderr."""
    res = subprocess.run(  # noqa: S603
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return res.returncode, res.stdout, res.stderr


def test_template(template_name: str, verbose: bool = False) -> bool:
    """Test a single template generation and test suite."""
    print("\n==================================================")
    print(f"  Testing Template: {template_name}")
    print("==================================================")

    with tempfile.TemporaryDirectory(prefix=f"test_{template_name}_") as tmpdir:
        dest = Path(tmpdir) / template_name

        # 1. Copier copy
        print("--> Instantiating via Copier dispatcher...")
        copier_cmd = [
            "uvx",
            "copier",
            "copy",
            "--defaults",
            "-d",
            f"template_type={template_name}",
            str(REPO_ROOT),
            str(dest),
        ]
        ret, stdout, stderr = run_command(copier_cmd, REPO_ROOT)
        if ret != 0:
            print(f"❌ Copier generation failed for {template_name}!")
            print(stderr)
            return False

        # 2. Assert structural files
        required_files = [
            dest / "AGENTS.md",
            dest / "pyproject.toml",
            dest / "justfile",
            dest / "README.md",
        ]
        if (dest / "packages").exists():
            required_files.extend([dest / "packages", dest / "assets"])
        else:
            required_files.extend([dest / "tests", dest / "src"])

        for req in required_files:
            if not req.exists():
                print(f"❌ Missing required file or directory: {req.name}")
                return False
        print("✅ Structural validation passed")

        # 3. Run Pytest
        print("--> Running test suite (`uv run --no-env-file pytest`)...")
        pytest_cmd = ["uv", "run", "--no-env-file", "pytest", "-v"]
        ret, stdout, stderr = run_command(pytest_cmd, dest)
        if ret != 0:
            print(f"❌ Pytest failed for {template_name}!")
            print(stdout)
            print(stderr)
            return False
        if verbose:
            print(stdout)
        print("✅ Pytest tests passed")

        # 4. Ruff Lint
        print("--> Running Ruff linter (`uvx --no-env-file ruff check .`)...")
        ruff_lint_cmd = ["uvx", "--no-env-file", "ruff", "check", "."]
        ret, stdout, stderr = run_command(ruff_lint_cmd, dest)
        if ret != 0:
            print(f"❌ Ruff lint check failed for {template_name}!")
            print(stdout)
            return False
        print("✅ Ruff linting passed")

        # 5. Ruff Format Check
        print("--> Running Ruff format check (`uvx --no-env-file ruff format --check .`)...")
        ruff_fmt_cmd = ["uvx", "--no-env-file", "ruff", "format", "--check", "."]
        ret, stdout, stderr = run_command(ruff_fmt_cmd, dest)
        if ret != 0:
            print(f"❌ Ruff format check failed for {template_name}!")
            print(stdout)
            return False
        print("✅ Ruff format check passed")

    print(f"🎉 Template '{template_name}' passed all verifications!")
    return True


def main() -> int:
    """Entry point for template integration testing."""
    parser = argparse.ArgumentParser(description="Test Copier project templates.")
    parser.add_argument(
        "--template",
        choices=TEMPLATES,
        help="Test a specific template only",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show verbose command output",
    )
    args = parser.parse_args()

    templates_to_test = [args.template] if args.template else TEMPLATES

    failed: list[str] = []
    for t in templates_to_test:
        success = test_template(t, verbose=args.verbose)
        if not success:
            failed.append(t)

    print("\n==================================================")
    print("  Template Test Summary")
    print("==================================================")
    if failed:
        print(f"❌ The following {len(failed)} template(s) failed:")
        for f in failed:
            print(f"  - {f}")
        return 1

    print(f"✅ All {len(templates_to_test)} template(s) verified successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
