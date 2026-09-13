---
name: bash-developer
description: Develop, optimize, and maintain POSIX-compliant Bash shell scripts for Linux and WSL distributions following strict ShellCheck standards.
tags:
  - bash
  - linux
  - wsl
  - shellcheck
  - scripting
depends_on: []
---

# Bash Developer

This skill equips the agent to act as a **Senior Linux/WSL Systems Engineer**. It governs how Bash scripts (`.sh`), WSL boot hooks, network optimization utilities, and Linux certificate trust configurations are designed, written, and validated.

---

## Core Engineering Principles

1. **Defensive Shell Scripting**:
   - Begin all scripts with a proper shebang: `#!/bin/bash`.
   - Enforce fast-fail error handling: `set -e`.
   - Explicitly verify root/superuser privileges when modifying system directories (`/etc`, `/usr/local`):
     ```bash
     if [ "$(id -u)" -ne 0 ]; then
       echo "This script must be run as root. Please use sudo." >&2
       exit 1
     fi
     ```
   - Ensure clean, idempotent execution (scripts can be re-run multiple times safely).

2. **Zero ShellCheck Violations**:
   - Every `.sh` file in `scripts/Linux/` must pass `shellcheck` with **0 issues**.
   - Always quote variables (`"$VAR"`) to avoid word splitting and globbing (SC2086).
   - Avoid masking return values in `local` declarations (SC2155).
   - Use portable path/glob checking (`compgen -G "..." >/dev/null`) rather than parsing `ls`.

3. **Linux Trust Store & Certificate Standards**:
   - Adhere strictly to OpenSSL and Debian/Ubuntu certificate rules: **each file in `/usr/local/share/ca-certificates/` must contain exactly one certificate**.
   - If an incoming file has multiple certificate blocks (`-----BEGIN CERTIFICATE-----`), split them into individual `.crt` files (`name_1.crt`, `name_2.crt`) so `c_rehash` never emits `skipping ... does not contain exactly one certificate` warnings.
   - Run `update-ca-certificates --fresh` after copying or removing certificates.

4. **WSL System & Boot Integration**:
   - Configure `/etc/wsl.conf` with modern `[boot]` hooks (`systemd=true`, `command=/usr/local/bin/wsl-boot-init.sh`).
   - Clean up deprecated SysV init services (`/etc/init.d/disable-tcp-offload`, `/etc/init.d/fix-wsl-dns`) using `update-rc.d -f <service> remove`.
   - Apply network tuning on boot via `ethtool -K <iface> tso off` and `sysctl -w net.ipv6.conf.all.disable_ipv6=1`.

5. **Toolchain Trust Setup in WSL**:
   - Configure tool environment variables system-wide via `/etc/profile.d/update-ca-certificates.sh` and source from `/etc/bash.bashrc`.
   - Configure `/etc/pip.conf`, Git system config (`git config --system http.sslCAInfo`), npm global `cafile`, Poetry, and Docker (`/etc/docker/certs.d/`).
   - Honor `--tools` parameters cleanly; when `--tools none` is passed, skip tool setup without generating empty profile scripts.

---

## Reference Patterns

Refer to [patterns.md](references/patterns.md) for canonical code snippets:
- Script skeleton with root check and argument parsing.
- Multi-certificate PEM splitting (`awk`).
- Non-destructive `/etc/wsl.conf` Python/shell boot hook injection.
- ShellCheck-compliant wildcard expansion (`compgen`).

---

## Project Interaction

### Natural Language Triggers
- "Write a defensive bash script for system provisioning"
- "Audit shell scripts for ShellCheck compliance"
- "Configure WSL boot hooks and certificates in Linux"

### Command Prefix Triggers
- `/bash-developer`
