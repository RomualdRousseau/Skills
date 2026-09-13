# Bash Engineering Patterns

## 1. Script Skeleton with Root Check & Argument Parsing

```bash
#!/bin/bash
set -e

# Verify root privileges
if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root. Please use sudo." >&2
  exit 1
fi

TOOLS=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --tools)
      TOOLS="$2"
      shift 2
      ;;
    --tools=*)
      TOOLS="${1#*=}"
      shift 1
      ;;
    *)
      shift 1
      ;;
  esac
done

SCRIPT_DIR=$(cd -- "$(dirname -- "$0")" && pwd)
```

## 2. Multi-Certificate Splitting (OpenSSL c_rehash Compliance)

```bash
# Each file in /usr/local/share/ca-certificates must contain exactly one certificate
CERT_COUNT=$(grep -c -- "-----BEGIN CERTIFICATE-----" "$CERT_FILE" || true)

if [ "$CERT_COUNT" -gt 1 ]; then
  echo "Splitting $CERT_COUNT certificates into individual single-cert files..."
  awk -v out="$DEST_DIR" 'BEGIN {c=0}
    /-----BEGIN CERTIFICATE-----/ {c++}
    { if (c>0) print > (out "/corporate_ca_" c ".crt") }' "$CERT_FILE"
else
  cp -f "$CERT_FILE" "$DEST_DIR/corporate_ca.crt"
fi

chmod 644 "$DEST_DIR"/corporate_ca*.crt
update-ca-certificates --fresh
```

## 3. ShellCheck-Compliant Wildcard Existence Check

```bash
# Good (SC-compliant, no word splitting, works when files do not exist):
if compgen -G "/usr/local/share/ca-certificates/corporate_ca*.crt" >/dev/null; then
  echo "Certificates found."
  rm -f /usr/local/share/ca-certificates/corporate_ca*.crt
fi
```

## 4. Modern /etc/wsl.conf Boot Hook Configuration

```bash
if command -v python3 >/dev/null 2>&1; then
  python3 -c '
import os

path = "/etc/wsl.conf"
lines = []
if os.path.exists(path):
    with open(path, "r") as f:
        lines = f.readlines()

new_lines = []
in_boot = False
boot_found = False
has_systemd = False
has_command = False

for line in lines:
    stripped = line.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        if in_boot:
            if not has_systemd: new_lines.append("systemd=true\n")
            if not has_command: new_lines.append("command=/usr/local/bin/wsl-boot-init.sh\n")
            in_boot = False
        if stripped.lower() == "[boot]":
            in_boot = True
            boot_found = True
        new_lines.append(line)
        continue
    if in_boot:
        if stripped.startswith("systemd"):
            new_lines.append("systemd=true\n")
            has_systemd = True
            continue
        elif stripped.startswith("command"):
            new_lines.append("command=/usr/local/bin/wsl-boot-init.sh\n")
            has_command = True
            continue
    new_lines.append(line)

if in_boot:
    if not has_systemd: new_lines.append("systemd=true\n")
    if not has_command: new_lines.append("command=/usr/local/bin/wsl-boot-init.sh\n")
elif not boot_found:
    if new_lines and not new_lines[-1].endswith("\n"):
        new_lines.append("\n")
    new_lines.append("\n[boot]\nsystemd=true\ncommand=/usr/local/bin/wsl-boot-init.sh\n")

with open(path, "w") as f:
    f.writelines(new_lines)
'
fi
```
