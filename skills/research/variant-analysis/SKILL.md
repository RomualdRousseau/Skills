---
name: variant-analysis
description: Perform interactive genomic variant analysis using the Variant Analysis Multi-Agent System. Use when the user wants to start a VCF analysis, check status, or query clinical assessments and population frequencies (gnomAD).
---

# Variant Analysis

## Overview
This skill automates the workflow for interacting with the Variant Analysis Multi-Agent System. It handles session management, authentication, and API communication for long-running VCF analysis and subsequent conversational queries.

## Workflow

### 1. Setup Session & Auth
Before starting, you **MUST** retrieve a valid Firebase token using the project's automated authentication script.

#### Requirements
- **uv**: The script must be executed via `uv run` to manage dependencies (google-auth, requests, etc.).
- **.env Settings**: The following variables must be configured in the project's `.env` file:
  - `GOOGLE_CLIENT_SECRET_PATH`: Absolute path to your Google OAuth2 client secret JSON file.
  - `GOOGLE_PROJECT_ID`: Your Google/Firebase project ID (e.g., `ai-innolab-...`).
  - `FIREBASE_API_KEY`: Your Firebase Web API Key (found in Firebase Project Settings).
  - `PUBLIC_API_URL`: The base URL for the Variant Analysis API.
  - `PUBLIC_HEALTH_URL`: The health check URL for the API.
  - `PUBLIC_GCS_URL`: The base GCS path for variant storage (e.g., `gs://my-bucket/path/`).

- **Session ID**: Omit for new sessions to allow the server to generate a unique ID. Include the returned `session_id` in subsequent requests (e.g., `analysis-<timestamp>`).
- **Firebase Token**: Execute the following command to get the token:
  ```bash
  uv run python .gemini/skills/variant-analysis/scripts/get_firebase_token.py
  ```
  **Procedural Note:** You must capture the stdout of this command and use it as the Bearer token in the `Authorization` header for all subsequent API requests. The script handles refresh logic automatically using a local cache. Do **not** look for a `firebase-id-token` file.

### 2. Phase 1: Start Analysis
To start an analysis, send a POST request to `/run` with the VCF path.
- **Input**: `Please analyze gs://path/to/variants.vcf.gz`
- **Reference**: See [api-docs.md](references/api-docs.md) for curl templates.

### 3. Phase 2: Wait & Get Results
The VEP process takes ~60-70 minutes.
- **Check Status**: `Is my VEP analysis complete?`
- **Generate Report**: The system automatically starts report generation (3-5 mins) once VEP is done.
- **Retrieve Report**: `Is my report ready? Please provide the clinical assessment.`

### 4. Phase 3: Conversational Querying
Once the report is ready, ask specific follow-up questions about genes or variants.
- **Example**: `Were any pathogenic variants found in the APOB gene?`

## GCS Storage
The system uses Google Cloud Storage for VCF files. The base storage path is defined by `PUBLIC_GCS_URL` in your `.env` file.
- **Usage**: When specifying VCF paths, ensure they are relative to this base URL or use the full `gs://` path if they are in the same project.

## API Details
For detailed endpoint information and JSON payloads, see [api-docs.md](references/api-docs.md).
