---
name: incremental-implementation
description: Delivers changes incrementally.
---

# Incremental Implementation

Build in thin vertical slices — implement, test, verify, commit, repeat.

## Slicing Strategies
- Vertical: one complete path through stack per slice (DB + API + UI)
- Contract-first: define API contract, then backend + frontend in parallel
- Risk-first: tackle riskiest piece first

## Rules
- One thing at a time, keep it compilable after each slice
- Feature flags for incomplete features
- Safe defaults, rollback-friendly
- Scope discipline: touch only what the task requires

## Increment Checklist: One thing done, tests pass, build succeeds, typecheck + lint pass, committed