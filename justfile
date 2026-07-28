# Skills Repository - Development and Verification Workflow

# Display all available recipes
default:
    @just --list

# Initialize development tools and pre-commit hooks
setup:
    uv run --no-env-file prek install

# Check skills directory for structural and naming homogeneity
lint-skills:
    python3 scripts/lint_skills.py

# Lint and check formatting of Python files locally
lint-code:
    uv run --no-env-file ruff check .
    uv run --no-env-file ruff format --check .

# Run all local lints (Code + Skills structure)
lint: lint-code lint-skills

# Format Python code locally using ruff
format:
    uv run --no-env-file ruff format .

# Scan for hardcoded credentials/secrets using a containerized Gitleaks instance
scan-secrets:
    @echo "Running Gitleaks secret scanner..."
    docker run --rm -v "$(pwd):/code" zricethezav/gitleaks:latest detect --source=/code -v

# Analyze Python code for OWASP Top 10 vulnerabilities inside an isolated container
scan-security path=".":
    @echo "Running Semgrep security static analysis on '{{path}}'..."
    docker run --rm -v "$(pwd):/src:ro" semgrep/semgrep semgrep scan --config=auto {{path}}

# Run full local checks + containerized secret and security scans
verify: lint scan-secrets scan-security
