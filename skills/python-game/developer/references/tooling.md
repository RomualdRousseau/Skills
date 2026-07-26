# Standard Tooling Templates

To maintain consistency across projects, use these templates for task management and automated quality control.

## 1. Justfile Template

Every project should have a minimal `justfile` for the most common tasks. A copyable template is also available at `assets/justfile`.

```just
# Default recipe: list all commands
default:
    @just --list

# Install dependencies
sync:
    uv sync --extra dev

# Run the game
play:
    uv run spacerace-play

# Run the test suite
test:
    uv run pytest

# Remove Python cache and test artifacts
clean:
    uvx pyclean . -d all
```

Add more recipes only when the project actually needs them (e.g., `lint`, `format`, `typecheck`).

## 2. Optional Pre-commit Configuration (prek)

For larger projects, use `prek` as the pre-commit tool. `prek` wraps the standard `pre-commit` hooks and is configured with the same `.pre-commit-config.yaml` file shown below. Use Astral's tools (`ruff` and `ty`) inside the hooks for fast and reliable checks.

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=1000]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: ty-check
        name: ty-check
        entry: uv run --no-env-file ty check
        language: system
        types: [python]
        pass_filenames: false
        stages: [pre-commit]
```

## 3. Modern Git Tooling

Maintain high repository standards with structured commit messages.

### Commit Messages

Use clear, concise messages focused on "why" rather than "what". Group related changes into single, logical commits.

- **Feature**: `feat: add wrap-around screen edges`
- **Fix**: `fix: prevent player from moving off-screen`
- **Refactor**: `refactor: move renderer logic to engine/raylib_engine.py`

### Automated Quality Control

Integrate with GitHub Actions to validate every pull request and commit:

```yaml
# .github/workflows/ci.yml
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: just test
```

### Git Hooks

For larger projects, use `prek` as the pre-commit tool to ensure that no broken code is ever committed to the repository.

```bash
# Install hooks
uv run --no-env-file prek install

# Run hooks manually
uv run --no-env-file prek run --all-files
```
