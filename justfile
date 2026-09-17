# Skills Repository - Development and Verification Workflow

# Display all available recipes
default:
    @just --list

# Initialize development tools and pre-commit hooks
setup:
    uvx --no-env-file prek install

# Check skills directory for structural and naming homogeneity
lint-skills:
    uv run python scripts/lint_skills.py

# Validate skill evaluations against agentskills.io schema
lint-evals:
    uv run python skills/skill-evaluator/scripts/eval_skill.py validate --all

# Scaffold starter evals.json for a skill
scaffold-evals skill:
    uv run python skills/skill-evaluator/scripts/eval_skill.py scaffold {{skill}}

# Benchmark an evaluation iteration directory
benchmark-evals dir:
    uv run python skills/skill-evaluator/scripts/eval_skill.py benchmark --iteration-dir {{dir}}

# Render a benchmark uplift report table
report-evals dir:
    uv run python skills/skill-evaluator/scripts/eval_skill.py report --iteration-dir {{dir}}

# Run type checking using Astral ty
type-check:
    uvx --no-env-file ty check

# Lint and check formatting of Python files locally
lint-code:
    uvx --no-env-file ruff check .
    uvx --no-env-file ruff format --check .
    uvx --no-env-file ty check

# Test all project templates by instantiating and verifying them
test-templates:
    uv run python scripts/test_templates.py

# Run unit tests
test-units:
    uv run pytest tests/

# Run all test suites
test: test-units test-templates

# Run all local lints (Code + Skills structure + Skill Evals)
lint: lint-code lint-skills lint-evals

# Format Python code locally using ruff
format:
    uvx --no-env-file ruff format .

# Scan for hardcoded credentials/secrets using a containerized Gitleaks instance
scan-secrets:
    @echo "Running Gitleaks secret scanner..."
    docker run --rm -v "$(pwd):/code" zricethezav/gitleaks:latest detect --source=/code -v

# Analyze Python code for OWASP Top 10 vulnerabilities inside an isolated container
scan-security path=".":
    @echo "Running Semgrep security static analysis on '{{path}}'..."
    docker run --rm -v "$(pwd):/src:ro" -v "/etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt:ro" -e SSL_CERTS_DIR="/etc/ssl/certs/ca-certificates.crt" -e REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt" semgrep/semgrep semgrep scan --config=auto {{path}}

# Run full local checks + containerized secret and security scans
verify: lint scan-secrets scan-security
