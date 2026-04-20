---
name: observability
description: Establishes standards for logging, metrics, and tracing using OpenTelemetry (OTel) to ensure production health and fast debugging.
---

# Observability & Reliability

This skill ensures systems are instrumented to provide deep visibility into their behavior, focusing on the "Three Pillars of Observability."

## 1. The Three Pillars
- **Logs (Structured Logging):** All application logs must be in JSON format. Include context fields (e.g., `trace_id`, `user_id`, `environment`). Stop using simple `print()` statements in production code.
- **Metrics (The Golden Signals):** Instrument services to track Latency, Traffic, Errors, and Saturation. Use Prometheus format.
- **Traces (OpenTelemetry):** Propagate context across service boundaries. Ensure every external API call or Database query creates a span.

## 2. Alerting & SLIs/SLOs
- **Actionable Alerts:** Alerts should only fire for user-facing degradation. Do not alert on high CPU if the service is auto-scaling normally.
- **SLIs/SLOs:** Define Service Level Indicators (e.g., "99% of requests complete in < 200ms") and alert on Error Budget burn rates.

## 3. Resilience Patterns
- **Timeouts & Retries:** Every external call must have a hard timeout. Use exponential backoff for retries.
- **Circuit Breakers:** Implement circuit breakers to prevent cascading failures when dependencies go down.

## Project Interaction

- **Trigger**: "Instrument [service] with OpenTelemetry spans"
- **Trigger**: "Setup structured JSON logging for [module]"
- **Trigger**: "Define the SLIs and SLOs for [application]"
- **Trigger**: "Implement a circuit breaker for the [API client]"
- **Trigger**: "Analyze the traces to find the bottleneck in [workflow]"

