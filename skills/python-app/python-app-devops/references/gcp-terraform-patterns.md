# GCP Terraform Patterns

## VPC Design (Shared vs. Project-Specific)
- **Shared VPC**: Use for large organizations to centralize networking.
- **Project-Specific VPC**: Use for isolation and simple environments.
- **Subnetting**: Define clear CIDR blocks; use private Google Access for internal-only resources.

## Service Selection: Cloud Run vs. GKE
- **Cloud Run**: Best for stateless, request-driven services; easy scaling, pay-per-use.
- **GKE**: Best for complex microservices with specific networking, stateful needs, or long-running processes.

## IAM Hardening
- **Principle of Least Privilege**: Grant permissions only to specific service accounts, not individuals.
- **Custom Roles**: Create granular roles for Terraform to manage only the required resources.
- **External Identities**: Avoid long-lived service account keys (see `gitlab-gcp-auth.md`).
