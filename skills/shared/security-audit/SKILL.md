---
name: security-audit
description: Enforces security best practices, static/dynamic analysis (SAST/DAST), and OWASP principles for high-integrity development.
---

# Security & Audit

This skill integrates security into the development lifecycle, focusing on automated scanning, secure coding, and proactive defense.

## 1. Secrets Management
- **No Hardcoded Secrets:** Never commit passwords, API keys, or tokens. Use environment variables or a secrets manager (e.g., HashiCorp Vault, GCP Secret Manager).
- **Scanning:** Enforce automated secret scanning (`gitleaks` or `trufflehog`) in pre-commit hooks and CI pipelines.

## 2. Application Security (AppSec)
- **SAST:** Integrate Static Application Security Testing (e.g., Bandit for Python, Semgrep) into CI pipelines. Fail builds on High/Critical findings.
- **Dependency Scanning:** Use `Dependabot` or `Renovate` to keep libraries up to date. Run `pip-audit` or `npm audit` on every build.
- **OWASP Top 10:** Defend against common vulnerabilities (Injection, Broken Authentication, SSRF, etc.). Validate and sanitize all external inputs.

## 3. Threat Modeling & Review
- **Assume Breach:** Design networks and permissions using the Principle of Least Privilege.
- **Code Reviews:** Security-sensitive changes (auth, cryptography, payment gateways) require two approvals.

## Project Interaction

- **Trigger**: "Perform a security audit of [module/file]"
- **Trigger**: "Setup automated secret scanning for the repo"
- **Trigger**: "Analyze the codebase for OWASP Top 10 vulnerabilities"
- **Trigger**: "Implement secure secrets management for [service]"
- **Trigger**: "Threat model the [feature/architecture]"

