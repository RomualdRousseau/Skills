import argparse
import os
import re
import sys
from typing import Any


def parse_frontmatter(fm_text: str) -> dict[str, Any]:
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


def load_skills(skills_root: str = "skills") -> dict[str, dict[str, Any]]:
    skills = {}
    if not os.path.isdir(skills_root):
        return skills

    for entry in sorted(os.listdir(skills_root)):
        skill_dir = os.path.join(skills_root, entry)
        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not (os.path.isdir(skill_dir) and os.path.isfile(skill_md)):
            continue

        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()

        parts = re.split(r"^---[\r\n]+", content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3:
            fm = parse_frontmatter(parts[1])
            skills[entry] = {
                "name": fm.get("name", entry),
                "description": fm.get("description", ""),
                "tags": fm.get("tags", []),
                "depends_on": fm.get("depends_on", []),
                "path": skill_dir,
            }

    return skills


def list_all_skills(skills: dict[str, dict[str, Any]]) -> None:
    print(f"{'Skill Name':<22} {'Depends On':<28} {'Tags'}")
    print("-" * 80)
    for name, info in sorted(skills.items()):
        deps = ", ".join(info["depends_on"]) if info["depends_on"] else "-"
        tags = ", ".join(info["tags"])
        print(f"{name:<22} {deps:<28} {tags}")


def filter_by_tag(skills: dict[str, dict[str, Any]], tag: str) -> None:
    matched = {name: info for name, info in skills.items() if tag.lower() in [t.lower() for t in info["tags"]]}
    print(f"Skills matching tag '{tag}' ({len(matched)} found):")
    print("-" * 80)
    list_all_skills(matched)


def show_tags_summary(skills: dict[str, dict[str, Any]]) -> None:
    tag_counts: dict[str, int] = {}
    for info in skills.values():
        for tag in info["tags"]:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    print(f"{'Tag':<25} {'Count'}")
    print("-" * 35)
    for tag, count in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"{tag:<25} {count}")


def show_skill_details(skills: dict[str, dict[str, Any]], skill_name: str) -> None:
    if skill_name not in skills:
        print(f"Error: Skill '{skill_name}' not found.", file=sys.stderr)
        sys.exit(1)

    info = skills[skill_name]
    print(f"Skill: {info['name']}")
    print(f"Path:  {info['path']}/SKILL.md")
    print(f"Description:\n  {info['description']}")
    print(f"Tags:\n  {', '.join(info['tags'])}")
    print(f"Direct Dependencies:\n  {', '.join(info['depends_on']) if info['depends_on'] else 'None'}")

    # Transitive dependencies
    def get_all_deps(current: str, visited: set[str]) -> set[str]:
        direct = skills.get(current, {}).get("depends_on", [])
        for d in direct:
            if d not in visited:
                visited.add(d)
                get_all_deps(d, visited)
        return visited

    all_deps = get_all_deps(skill_name, set())
    if all_deps:
        print(f"Transitive Dependencies (to load together):\n  {', '.join(sorted(all_deps))}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Query and catalog skills by tags and dependencies.")
    parser.add_argument("--tag", "-t", type=str, help="Filter skills by tag")
    parser.add_argument("--skill", "-s", type=str, help="Show details and dependency tree for a skill")
    parser.add_argument("--tags", action="store_true", help="List all available tags with skill counts")

    args = parser.parse_args()
    skills = load_skills()

    if args.tags:
        show_tags_summary(skills)
    elif args.tag:
        filter_by_tag(skills, args.tag)
    elif args.skill:
        show_skill_details(skills, args.skill)
    else:
        list_all_skills(skills)


if __name__ == "__main__":
    main()
