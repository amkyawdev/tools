---
name: shipping-and-launch
description: Prepares production launches.
---

# Shipping and Launch

Ship with confidence. Every launch should be reversible, observable, and incremental.

## Pre-Launch Checklist: Code quality, security, performance, accessibility, infrastructure, documentation

## Feature Flag Strategy: Deploy OFF → enable for team → gradual rollout (5%→25%→50%→100%) → clean up

## Staged Rollout: Staging → production (flag OFF) → team → canary 5% → increase → full rollout

## Monitoring: Error rate, latency, request volume, active users, Core Web Vitals, client JS errors

## Rollback: Feature flag < 1 min, redeploy < 5 min, DB rollback < 15 min

## Rollback Triggers: Error rate > 2x baseline, p95 latency > 50%, data integrity issues