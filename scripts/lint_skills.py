import os
import re
import sys
from typing import Any


def parse_frontmatter(fm_text: str) -> dict[str, Any]:
    """Parse simple YAML frontmatter without external dependencies."""
    data: dict[str, Any] = {}
    current_key: str | None = None

    for line in fm_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- "):
            item = stripped[2:].strip().strip("\"'")
            if current_key:
                if not isinstance(data.get(current_key), list):
                    data[current_key] = []
                data[current_key].append(item)
        elif ":" in stripped:
            key, val = stripped.split(":", 1)
            current_key = key.strip().lower()
            val = val.strip().strip("\"'")
            if val == "[]":
                data[current_key] = []
            elif val:
                data[current_key] = val
            else:
                data[current_key] = []

    return data


def lint_skills(skills_root: str = "skills") -> bool:
    if not os.path.isdir(skills_root):
        print(f"Error: Skills root directory '{skills_root}' does not exist.")
        return False

    violations: list[str] = []
    scanned_count = 0

    all_skill_names = set()
    skill_dirs = []

    # 1. Discover all flat skill directories
    for entry in sorted(os.listdir(skills_root)):
        entry_path = os.path.join(skills_root, entry)
        if os.path.isdir(entry_path) and not entry.startswith((".", "_")):
            all_skill_names.add(entry)
            skill_dirs.append((entry, entry_path))

    # 2. Validate each skill
    for skill_name, skill_path in skill_dirs:
        scanned_count += 1
        rel_skill_path = os.path.relpath(skill_path)

        skill_md_path = os.path.join(skill_path, "SKILL.md")
        if not os.path.isfile(skill_md_path):
            violations.append(f"Missing mandatory 'SKILL.md' file in '{rel_skill_path}'.")
            continue

        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check YAML frontmatter presence
        has_frontmatter = content.startswith("---\n") or content.startswith("---\r\n")
        if not has_frontmatter:
            violations.append(f"'{rel_skill_path}/SKILL.md' is missing YAML frontmatter separators ('---').")
            continue

        parts = re.split(r"^---[\r\n]+", content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) < 3:
            violations.append(f"Failed to parse YAML frontmatter in '{rel_skill_path}/SKILL.md'.")
            continue

        fm_text = parts[1]
        body_text = parts[2]
        fm_data = parse_frontmatter(fm_text)

        # Check 'name'
        fm_name = fm_data.get("name")
        if not fm_name or not isinstance(fm_name, str):
            violations.append(f"Missing required 'name' field in frontmatter of '{rel_skill_path}/SKILL.md'.")
        elif fm_name != skill_name:
            violations.append(
                f"Frontmatter 'name: {fm_name}' in '{rel_skill_path}/SKILL.md' does not match directory '{skill_name}'."
            )

        # Check 'description'
        fm_desc = fm_data.get("description")
        if not fm_desc or not isinstance(fm_desc, str) or not fm_desc.strip():
            violations.append(f"Missing or empty 'description' in frontmatter of '{rel_skill_path}/SKILL.md'.")

        # Check 'tags'
        fm_tags = fm_data.get("tags")
        if fm_tags is None or not isinstance(fm_tags, list) or len(fm_tags) == 0:
            violations.append(f"Missing or empty 'tags' list in frontmatter of '{rel_skill_path}/SKILL.md'.")
        else:
            for tag in fm_tags:
                if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", tag):
                    violations.append(
                        f"Invalid tag '{tag}' in '{rel_skill_path}/SKILL.md'. Tags must be lowercase alphanumeric and hyphens."
                    )

        # Check 'depends_on'
        fm_depends = fm_data.get("depends_on")
        if fm_depends is None or not isinstance(fm_depends, list):
            violations.append(f"Missing 'depends_on' list in frontmatter of '{rel_skill_path}/SKILL.md'.")
        else:
            for dep in fm_depends:
                if dep not in all_skill_names:
                    violations.append(f"Unknown dependency '{dep}' in 'depends_on' of '{rel_skill_path}/SKILL.md'.")

        # Check for Project Interaction triggers section
        has_trigger_header = bool(re.search(r"^#+\s+Project\s+Interactions?", body_text, re.IGNORECASE | re.MULTILINE))
        if not has_trigger_header:
            violations.append(f"'{rel_skill_path}/SKILL.md' is missing required 'Project Interaction' section.")

        # Check for broken relative references inside SKILL.md
        clean_content = re.sub(r"```[\s\S]*?```", "", content)
        clean_content = re.sub(r"`[^`]*?`", "", clean_content)

        links = re.findall(r"\[.*?\]\((.*?)\)", clean_content)
        for link in links:
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue

            clean_link = link.split("#")[0]
            if not clean_link:
                continue

            target_path = os.path.join(skill_path, clean_link)
            if ".agents/skills" in clean_link:
                clean_link_resolved = clean_link.replace(".agents/", "")
                target_path = os.path.join(os.getcwd(), clean_link_resolved)

            if not os.path.exists(target_path):
                violations.append(
                    f"Broken reference inside '{rel_skill_path}/SKILL.md': '{link}' (File not found on disk)."
                )

    # Print Report
    print("==================================================")
    print("               SKILLS LINT REPORT                 ")
    print("==================================================")
    print(f"Total skills scanned: {scanned_count}")
    print("--------------------------------------------------")

    if violations:
        print(f"FAIL: Found {len(violations)} homogeneity violations:")
        for violation in violations:
            print(f"  - {violation}")
        print("==================================================")
        return False
    else:
        print("SUCCESS: All skills adhere to flat naming, metadata, and structural standards!")
        print("==================================================")
        return True


if __name__ == "__main__":
    success = lint_skills()
    if not success:
        sys.exit(1)
    sys.exit(0)
