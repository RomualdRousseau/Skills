import os
import re
import sys


def lint_skills(skills_root="skills"):
    if not os.path.isdir(skills_root):
        print(f"Error: Skills root directory '{skills_root}' does not exist.")
        return False

    violations = []
    scanned_count = 0

    # Traverse skills/<domain>/<skill-dir>
    for domain in sorted(os.listdir(skills_root)):
        domain_path = os.path.join(skills_root, domain)
        if not os.path.isdir(domain_path):
            continue

        for skill in sorted(os.listdir(domain_path)):
            skill_path = os.path.join(domain_path, skill)
            if not os.path.isdir(skill_path):
                continue

            scanned_count += 1
            rel_skill_path = os.path.relpath(skill_path)

            # 1. Check directory prefix naming convention
            expected_prefix = f"{domain}-"
            if not skill.startswith(expected_prefix):
                violations.append(
                    f"Directory '{rel_skill_path}' does not begin with its domain prefix '{expected_prefix}'."
                )

            skill_md_path = os.path.join(skill_path, "SKILL.md")
            if not os.path.isfile(skill_md_path):
                violations.append(f"Missing mandatory 'SKILL.md' file in '{rel_skill_path}'.")
                continue

            # Parse SKILL.md
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 2. Parse YAML Frontmatter
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

            fm_fields = {}
            for line in fm_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm_fields[k.strip().lower()] = v.strip()

            # Check Frontmatter Name Match
            fm_name = fm_fields.get("name")
            if not fm_name:
                violations.append(f"Missing required 'name' field in frontmatter of '{rel_skill_path}/SKILL.md'.")
            elif fm_name != skill:
                violations.append(
                    f"Frontmatter 'name: {fm_name}' in '{rel_skill_path}/SKILL.md' does not match directory name '{skill}'."
                )

            # 3. Check for Project Interaction triggers section
            has_trigger_header = bool(
                re.search(r"^#+\s+Project\s+Interaction", body_text, re.IGNORECASE | re.MULTILINE)
            )
            if not has_trigger_header:
                violations.append(
                    f"'{rel_skill_path}/SKILL.md' is missing required 'Project Interaction' or 'Project Interactions' section."
                )

            # 4. Check for broken relative references inside SKILL.md
            # Strip code blocks and inline code to avoid checking example links inside backticks
            clean_content = re.sub(r"```[\s\S]*?```", "", content)
            clean_content = re.sub(r"`[^`]*?`", "", clean_content)

            # Matches standard markdown links like [label](path)
            links = re.findall(r"\[.*?\]\((.*?)\)", clean_content)
            for link in links:
                # Skip external links and web addresses
                if link.startswith(("http://", "https://", "mailto:", "#")):
                    continue

                # Remove anchors if present
                clean_link = link.split("#")[0]
                if not clean_link:
                    continue

                # Check path relative to skill folder
                target_path = os.path.join(skill_path, clean_link)
                # Also handle potential global relative references
                if ".agents/skills" in clean_link:
                    # Clean up prefix references
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
        print("SUCCESS: All skills adhere to prefix, naming, and structural standards!")
        print("==================================================")
        return True


if __name__ == "__main__":
    success = lint_skills()
    if not success:
        sys.exit(1)
    sys.exit(0)
