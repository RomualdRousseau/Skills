---
name: powershell-developer
description: Develop, refactor, and test enterprise PowerShell modules, scripts, and Pester test suites following strict repository standards.
tags:
  - powershell
  - modules
  - pester
  - psscriptanalyzer
  - automation
depends_on: []
---

# PowerShell Developer

This skill equips the agent to act as a **Senior PowerShell Engineer**. It governs how PowerShell scripts, modules (`.psm1`), module manifests (`.psd1`), and Pester tests are designed, structured, and validated.

---

## Core Engineering Principles

1. **Strict Advanced Functions**:
   - Always decorate public and module functions with `[CmdletBinding()]`.
   - Explicitly type all parameters in `param(...)`.
   - Use validation attributes (`[ValidateSet()]`, `[ValidateNotNullOrEmpty()]`, etc.) to enforce constraints at binding time.
   - Use native hashtable parameter splatting (`& $cmd @params`) rather than `Invoke-Expression` or string concatenation.

2. **Module Architecture & Manifests**:
   - Organize domain logic into standalone modules under `scripts/Modules/<ModuleName>/`.
   - Maintain a companion `.psd1` module manifest alongside every `.psm1`.
   - Explicitly export public functions via `FunctionsToExport` and aliases via `AliasesToExport` in the manifest.
   - Restrict module member exports in `.psm1` using `Export-ModuleMember`.

3. **Config-Driven Design (`Settings.psd1`)**:
   - All defaults, paths, and tool targets must be sourced from configuration files.
   - Never hardcode file paths or passwords in code.
   - Never rely on legacy environment variable triggers (`ENABLE_*`).
   - Treat `java` as a standard member of `Tools.SupportedTools` without bespoke flags.

4. **Cross-Version & WSL Compatibility**:
   - Code must execute reliably on both **PowerShell 7+** and **Windows PowerShell 5.1**.
   - Strip UTF-16LE null bytes from `wsl.exe` output (`-replace "\x00", ""`).
   - Resolve Windows paths to WSL paths using `wslpath` or regex translation.

5. **Security & Static Analysis**:
   - Must achieve **0 issues** against `PSScriptAnalyzerSettings.psd1`.
   - Never hardcode plaintext passwords in files committed to git (`JavaKeystorePass` must remain `""` in repo).

6. **Pester 5 Testing**:
   - Unit tests must be non-mutating (zero permanent modifications to host certificate stores, user PATH, or user environment).
   - Use isolated temporary directories (`$env:TEMP\...\`) with `BeforeAll` / `AfterAll` cleanup blocks.

---

## Reference Patterns

Refer to [patterns.md](references/patterns.md) for canonical code snippets:
- Advanced function with typed parameter splatting.
- Settings loader pattern (`Import-PowerShellDataFile`).
- WSL CLI invocation and null-byte sanitization.
- Non-mutating Pester test structure.

---

## Project Interaction

### Natural Language Triggers
- "Develop a PowerShell advanced module with PSScriptAnalyzer compliance"
- "Author Pester unit tests for PowerShell cmdlets"
- "Refactor PowerShell automation scripts"

### Command Prefix Triggers
- `/powershell-developer`
