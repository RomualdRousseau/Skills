import os
import re
import shutil
import sys


def build_file_map(src_dir):
    """Builds a map of (filename_with_ext) and (filename_no_ext) -> path relative to src_dir."""
    file_map = {}
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".md") or file.endswith(".html"):
                rel_path = os.path.relpath(os.path.join(root, file), src_dir)
                rel_path = rel_path.replace("\\", "/")

                # Always store with full name
                file_map[file] = rel_path

                # Store without extension if not already present or if it's a .md (to prioritize .md for wikilinks)
                name_no_ext = os.path.splitext(file)[0]
                if name_no_ext not in file_map or file.endswith(".md"):
                    file_map[name_no_ext] = rel_path

    return file_map


def convert_wikilinks(content, file_map, current_file_rel_dir):
    """
    Match [[page]] or [[page|alias]]
    Uses file_map to find the correct path from root, then computes relative path.
    """

    def replace_link(match):
        inner = match.group(1)
        if "|" in inner:
            page_name, alias = inner.split("|", 1)
        else:
            page_name, alias = inner, inner

        lookup_name = page_name
        if lookup_name not in file_map:
            lookup_name = os.path.splitext(page_name)[0]

        if lookup_name in file_map:
            target_path = file_map[lookup_name]
            # Convert to relative path
            rel_to_target = os.path.relpath(target_path, current_file_rel_dir)
            rel_to_target = rel_to_target.replace("\\", "/")

            # Remove .md extension for Zensical/MkDocs cleaner links
            if rel_to_target.endswith(".md"):
                rel_to_target = rel_to_target[:-3] + "/"

            return f"[{alias}]({rel_to_target})"
        else:
            return f"[{alias}]({page_name}/)"

    # Split frontmatter and body
    parts = content.split("---\n", 2)
    if len(parts) >= 3 and content.startswith("---\n"):
        frontmatter_raw = parts[1]
        body = parts[2]

        clean_frontmatter = (
            frontmatter_raw.replace("[[", "")
            .replace("]]", "")
            .replace("[", "")
            .replace("]", "")
            .replace('"', "")
            .replace("'", "")
        )

        new_content = f"---\n{clean_frontmatter}---\n"
        new_content += re.sub(r"\[\[(.*?)\]\]", replace_link, body)
        return new_content
    else:
        return re.sub(r"\[\[(.*?)\]\]", replace_link, content)


def preprocess(src_dir, dest_dir):
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist.")
        return

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    file_map = build_file_map(src_dir)

    shutil.copytree(src_dir, dest_dir)

    for root, dirs, files in os.walk(dest_dir):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                rel_file_path = os.path.relpath(path, dest_dir)
                current_file_rel_dir = os.path.dirname(rel_file_path)

                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = convert_wikilinks(content, file_map, current_file_rel_dir)

                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "wiki"
    dest = sys.argv[2] if len(sys.argv) > 2 else "build_docs"

    preprocess(src, dest)
    print(f"Preprocessed {src} into {dest} with proper relative links.")
