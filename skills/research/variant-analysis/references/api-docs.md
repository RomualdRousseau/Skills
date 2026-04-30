# Variant Analysis API Reference

## Base URL

Defined by `PUBLIC_API_URL` in `.env`.
(Default: `http://localhost:8080/api`)

## Health URL

Defined by `PUBLIC_HEALTH_URL` in `.env`.
(Default: `http://localhost:8080/health`)

## Storage (GCS)

Defined by `PUBLIC_GCS_URL` in `.env`.
(Example: `gs://ai-innolab-brain-genomics/`)

## Authentication

All requests require a Bearer token in the `Authorization` header.

```bash
Authorization: Bearer <FIREBASE_TOKEN>
```

## Endpoints

### POST /run

Main endpoint for all interactive tasks.

#### Request Body

```json
{
  "session_id": {
    "type": "string",
    "optional": true,
    "description": "Omit this parameter when starting a NEW session. Include it to continue an existing session."
  },
  "input_text": {
    "type": "string",
    "required": true
  }
}
```

#### Examples

**1. Start Analysis (New Session)**

```json
{
  "input_text": "Please analyze ${PUBLIC_GCS_URL}path/to/variant.vcf.gz"
}
```

**2. Check Status (Existing Session)**

```json
{
  "session_id": "session-123",
  "input_text": "Is my VEP analysis complete?"
}
```

**3. Get Report**

```json
{
  "session_id": "session-123",
  "input_text": "Is my report ready? Please provide the clinical assessment."
}
```

**4. Follow-up Query**

```json
{
  "session_id": "session-123",
  "input_text": "Were any pathogenic variants found in the APOB gene?"
}
```

## gnomAD Data Format

The system returns population frequencies in the following format:

```json
{
  "variant": "2:21006087:C>T",
  "source": "gnomAD_v2",
  "global_af": 0.000064,
  "carrier_frequency": "1 in 15,686",
  "population_frequencies": {
    "african": 0.0,
    "european_non_finnish": 0.000065,
    "east_asian": 0.0,
    "latino": 0.0
  },
  "homozygotes": 0,
  "clinical_interpretation": "European-specific, very rare, high penetrance suspected"
}
```
