import os
import re
import shutil
import sys

def build_file_map(src_dir):
    """Builds a map of filename (without extension) -> path relative to src_dir."""
    file_map = {}
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.md'):
                name = os.path.splitext(file)[0]
                rel_path = os.path.relpath(os.path.join(root, file), src_dir)
                # Convert backslashes to forward slashes for URL/Posix compatibility
                rel_path = rel_path.replace('\\', '/')
                # We store the first one we find. In case of duplicates, 
                # Obsidian usually resolves to one, we'll do the same.
                if name not in file_map:
                    file_map[name] = rel_path
    return file_map

def convert_wikilinks(content, file_map):
    """
    Match [[page]] or [[page|alias]]
    Uses file_map to find the correct path from root.
    """
    
    def replace_link(match):
        inner = match.group(1)
        if '|' in inner:
            page_name, alias = inner.split('|', 1)
        else:
            page_name, alias = inner, inner
        
        # Look up the page in our map
        # We strip potential .md from the page_name if the user included it
        lookup_name = os.path.splitext(page_name)[0]
        
        if lookup_name in file_map:
            target_path = file_map[lookup_name]
            # Strip .md for pretty URLs
            pretty_path = os.path.splitext(target_path)[0]
            
            # Handle index.md as the root of its directory
            if pretty_path.endswith('index'):
                pretty_path = pretty_path[:-5]
            
            # Ensure it starts and ends with a slash for root-relative pretty URLs
            return f"[{alias}](/{pretty_path}/)"
        else:
            # Fallback if page not found: keep it as text or relative
            # For now, let's keep it as a relative link to the name + .md
            # which is what it was doing before.
            return f"[{alias}]({page_name}.md)"

    return re.sub(r'\[\[(.*?)\]\]', replace_link, content)

def preprocess(src_dir, dest_dir):
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist.")
        return

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    # First, build the global map of files
    file_map = build_file_map(src_dir)
    
    shutil.copytree(src_dir, dest_dir)
    
    for root, dirs, files in os.walk(dest_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = convert_wikilinks(content, file_map)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "wiki"
    dest = sys.argv[2] if len(sys.argv) > 2 else "build_docs"
    
    preprocess(src, dest)
    print(f"Preprocessed {src} into {dest} with root-relative links.")
