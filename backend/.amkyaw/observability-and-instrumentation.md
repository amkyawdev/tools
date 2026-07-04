---
name: observability-and-instrumentation
description: Instruments code for production visibility.
---

# Observability and Instrumentation

Code you can't observe is code you can't operate.

## Process
1. Define "working" — 2-4 on-call questions the feature must answer
2. Pick signals: structured logs (why), metrics (how often/fast), traces (where time went)
3. Structured logging: JSON with stable event names + correlation IDs
4. Metrics: RED (Rate/Errors/Duration) for services, USE (Utilization/Saturation/Errors) for resources
5. Distributed tracing: OpenTelemetry auto-instrumentation + manual spans for internal units
6. Alerting: symptom-based (not cause-based), actionable, runbook-linked
7. Verify: force errors in staging, confirm telemetry appears