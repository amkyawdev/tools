---
name: debugging-and-error-recovery
description: Systematic root-cause debugging.
---
# Debugging and Error Recovery

Stop-the-Line: STOP → PRESERVE → DIAGNOSE → FIX → GUARD → RESUME.

Triage: Reproduce → Localize → Reduce → Fix Root Cause → Guard (regression test) → Verify.

Error Patterns: Test fail (check shared state), Build fail (types/imports/config), Runtime (null, network, render).
Safe Fallbacks: default + warning, graceful degradation, error boundaries with reporting.