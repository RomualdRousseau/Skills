import os
import re
import sys

def lint_wiki(wiki_dir):
    if not os.path.exists(wiki_dir):
        print(f"Error: Wiki directory '{wiki_dir}' does not exist.")
        return False

    # Collect all markdown files
    md_files = []
    for root, dirs, files in os.walk(wiki_dir):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, wiki_dir).replace("\\", "/")
                md_files.append((full_path, rel_path, file))

    # Build file mappings
    # 1. Base name without ext -> relative path (e.g., "orbit" -> "projects/orbit.md")
    # 2. File name with ext -> relative path (e.g., "orbit.md" -> "projects/orbit.md")
    # 3. Rel path from wiki/ -> relative path
    base_to_rel = {}
    name_to_rel = {}
    rel_to_rel = {}

    for full, rel, filename in md_files:
        base_name = os.path.splitext(filename)[0]
        base_to_rel[base_name] = rel
        name_to_rel[filename] = rel
        rel_to_rel[rel] = rel
        # Also map without .md extension
        if rel.endswith(".md"):
            rel_to_rel[rel[:-3]] = rel

    # Stats / results
    broken_links = {}
    orphans = set()
    unindexed = []
    invalid_frontmatter = []
    all_incoming_links = {rel: set() for _, rel, _ in md_files}

    # Helper to check if link target exists
    def find_target(target):
        # target might be "orbit", "projects/orbit.md", "projects/orbit", etc.
        target_clean = target.strip()
        
        # 1. Direct match in base_to_rel
        if target_clean in base_to_rel:
            return base_to_rel[target_clean]
        # 2. Match in rel_to_rel
        if target_clean in rel_to_rel:
            return rel_to_rel[target_clean]
        # 3. Match in name_to_rel
        if target_clean in name_to_rel:
            return name_to_rel[target_clean]
            
        # Try lowercase variants
        for k, v in base_to_rel.items():
            if k.lower() == target_clean.lower():
                return v
        for k, v in rel_to_rel.items():
            if k.lower() == target_clean.lower():
                return v
                
        return None

    # Parse index.md to track index references
    index_rel = "index.md"
    index_links = set()

    for full_path, rel_path, filename in md_files:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Parse frontmatter
        has_frontmatter = content.startswith("---\n") or content.startswith("---\r\n")
        fm_fields = {}
        if has_frontmatter:
            parts = re.split(r'^---[\r\n]+', content, maxsplit=2, flags=re.MULTILINE)
            # parts[0] is empty, parts[1] is frontmatter, parts[2] is body
            if len(parts) >= 3:
                fm_text = parts[1]
                body_text = parts[2]
                for line in fm_text.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        fm_fields[k.strip()] = v.strip()
            else:
                body_text = content
                has_frontmatter = False
        else:
            body_text = content

        # Exclude index.md and some custom files from strict frontmatter validation if they don't have type
        is_index = rel_path == "index.md"
        
        if not is_index:
            if not has_frontmatter:
                invalid_frontmatter.append((rel_path, "Missing YAML frontmatter"))
            else:
                required = ["title", "type", "updated"]
                missing = [field for field in required if field not in fm_fields]
                if missing:
                    invalid_frontmatter.append((rel_path, f"Missing required fields: {', '.join(missing)}"))
                elif fm_fields.get("type") not in ["source", "feature", "product", "persona", "concept", "style", "analysis", "overview", "log", "glossary", "project"]:
                    invalid_frontmatter.append((rel_path, f"Unknown type field value: '{fm_fields.get('type')}'"))

        # 2. Extract wikilinks from body and frontmatter
        # Include both standard body wikilinks [[link]] and frontmatter sources formatted as "[[link]]"
        all_text_to_search = content
        links = re.findall(r'\[\[(.*?)\]\]', all_text_to_search)

        for link in links:
            # Handle aliases like [[page|alias]]
            target = link.split("|")[0].strip()
            
            # Skip empty or external links if any
            if not target:
                continue

            target_rel = find_target(target)
            if target_rel:
                # Record incoming link (avoid self-linking)
                if target_rel != rel_path:
                    all_incoming_links[target_rel].add(rel_path)
                if rel_path == index_rel:
                    index_links.add(target_rel)
            else:
                # Record broken link
                if rel_path not in broken_links:
                    broken_links[rel_path] = []
                broken_links[rel_path].append(target)

    # 3. Identify Orphans
    # We define an orphan as any page with 0 incoming links.
    # Exclude system files: index.md, overview.md, glossary.md, log.md
    system_files = {"index.md", "overview.md", "glossary.md", "log.md"}
    for rel_path, incoming in all_incoming_links.items():
        if rel_path not in system_files and len(incoming) == 0:
            orphans.add(rel_path)

    # 4. Identify Unindexed Pages
    # Any page not in system_files and not linked by index.md is unindexed
    for _, rel_path, _ in md_files:
        if rel_path not in system_files and rel_path != index_rel:
            if rel_path not in index_links:
                unindexed.append(rel_path)

    # Print Report
    print("==================================================")
    print("                WIKI LINT REPORT                  ")
    print("==================================================")
    print(f"Total markdown files scanned: {len(md_files)}")
    print("--------------------------------------------------")

    # 1. Invalid Frontmatter
    print(f"\n[1] Frontmatter Violations ({len(invalid_frontmatter)}):")
    if invalid_frontmatter:
        for path, err in sorted(invalid_frontmatter):
            print(f"  - {path}: {err}")
    else:
        print("  ✓ All files have valid YAML frontmatter structures!")

    # 2. Broken Links
    total_broken = sum(len(links) for links in broken_links.values())
    print(f"\n[2] Broken Wikilinks ({total_broken}):")
    if broken_links:
        for path, targets in sorted(broken_links.items()):
            print(f"  - {path}:")
            for target in sorted(set(targets)):
                print(f"    * Broken link: [[{target}]]")
    else:
        print("  ✓ No broken wikilinks found!")

    # 3. Unindexed Pages
    print(f"\n[3] Unindexed Pages ({len(unindexed)}):")
    if unindexed:
        for path in sorted(unindexed):
            print(f"  - {path} (Not linked in index.md)")
    else:
        print("  ✓ All pages are referenced in index.md!")

    # 4. Orphan Pages
    print(f"\n[4] Orphan Pages ({len(orphans)}):")
    if orphans:
        for path in sorted(orphans):
            print(f"  - {path} (0 inbound links from other pages)")
    else:
        print("  ✓ No orphan pages found!")

    print("\n==================================================")
    
    # Return true if clean, false if any issues found
    is_clean = not (invalid_frontmatter or broken_links or unindexed or orphans)
    return is_clean

if __name__ == "__main__":
    wiki_path = "wiki"
    lint_wiki(wiki_path)
