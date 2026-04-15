---
name: devops
description: DevOps guidance for deploying applications to GCP using Terraform and GitLab CI/CD. Use when designing infrastructure, CI/CD pipelines, or implementing Workload Identity Federation (WIF).
---

# DevOps GCP & GitLab CI/CD

This skill provides a comprehensive workflow and reusable components for deploying infrastructure and applications to GCP using Terraform and GitLab.

## Quick Start: Initialize a New Project

Use the `init_project.py` script to scaffold a new repository with Terraform and GitLab CI/CD:

```bash
python scripts/init_project.py <project_name> <gcp_project_id> <region> <state_bucket>
```

This will create:
- `terraform/`: Base HCL files (`main.tf`, `providers.tf`, `variables.tf`, `outputs.tf`).
- `.gitlab-ci.yml`: Standard pipeline with `validate`, `plan`, `apply`, and `destroy` stages.

## Core Workflows

### Infrastructure Design
- Follow the patterns in [GCP Terraform Patterns](references/gcp-terraform-patterns.md).
- Use project-specific VPCs for isolation unless a Shared VPC is required.
- Prefer Cloud Run for stateless services and GKE for complex microservices.

### Secure Authentication (WIF)
Avoid long-lived service account keys. Implement Workload Identity Federation (WIF) by following [GitLab to GCP Authentication](references/gitlab-gcp-auth.md).

### CI/CD Pipeline Management
- **Validation**: Every commit triggers `terraform validate`.
- **Planning**: Every MR triggers `terraform plan`.
- **Deployment**: Manual approval on the `main` branch triggers `terraform apply`.
- **Cleanup**: Manual `terraform destroy` is available for experimental environments.

## Resources
- **Assets**:
    - `terraform-base/`: Pre-configured provider and variable templates.
    - `gitlab-ci-terraform.yml`: Robust CI/CD pipeline template.
- **References**:
    - `gcp-terraform-patterns.md`: Architecture best practices.
    - `gitlab-gcp-auth.md`: Step-by-step WIF guide.
