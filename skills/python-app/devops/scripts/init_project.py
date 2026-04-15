import os
import shutil
import sys

def init_project(project_name, project_id, region, state_bucket):
    # Create target directory
    if os.path.exists(project_name):
        print(f"Error: Directory {project_name} already exists.")
        sys.exit(1)
    
    os.makedirs(project_name)
    
    # Path to assets (relative to skill root)
    # The skill root is the directory containing SKILL.md
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_path = os.path.join(skill_root, "assets")
    
    # Copy Terraform base
    tf_base_src = os.path.join(assets_path, "terraform-base")
    tf_base_dst = os.path.join(project_name, "terraform")
    shutil.copytree(tf_base_src, tf_base_dst)
    
    # Update providers.tf if needed (currently it uses variables)
    
    # Copy and update .gitlab-ci.yml
    gitlab_ci_src = os.path.join(assets_path, "gitlab-ci-terraform.yml")
    gitlab_ci_dst = os.path.join(project_name, ".gitlab-ci.yml")
    
    with open(gitlab_ci_src, 'r') as f:
        content = f.read()
    
    content = content.replace('my-terraform-state-bucket', state_bucket)
    content = content.replace('my-gcp-project-id', project_id)
    
    with open(gitlab_ci_dst, 'w') as f:
        f.write(content)
    
    print(f"Project {project_name} initialized successfully.")
    print(f"Terraform config: {tf_base_dst}")
    print(f"GitLab CI: {gitlab_ci_dst}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python init_project.py <project_name> <project_id> <region> <state_bucket>")
        sys.exit(1)
    
    init_project(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
