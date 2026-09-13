# GitLab to GCP Authentication (WIF)

Workload Identity Federation (WIF) allows GitLab CI/CD to authenticate with GCP without using long-lived service account keys.

## Step 1: Create a Workload Identity Pool
```hcl
resource "google_iam_workload_identity_pool" "gitlab_pool" {
  workload_identity_pool_id = "gitlab-pool"
}
```

## Step 2: Create a Workload Identity Provider
```hcl
resource "google_iam_workload_identity_pool_provider" "gitlab_provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.gitlab_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "gitlab-provider"
  attribute_mapping = {
    "google.subject"           = "assertion.sub"
    "attribute.project_path"   = "assertion.project_path"
    "attribute.project_id"     = "assertion.project_id"
    "attribute.namespace_id"   = "assertion.namespace_id"
    "attribute.pipeline_source" = "assertion.pipeline_source"
  }
  oidc {
    issuer_uri = "https://gitlab.com"
  }
}
```

## Step 3: Grant Permissions to the Service Account
```hcl
resource "google_service_account_iam_member" "gitlab_sa_wif" {
  service_account_id = google_service_account.terraform_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.gitlab_pool.name}/attribute.project_id/${GITLAB_PROJECT_ID}"
}
```
