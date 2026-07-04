---
name: spec-driven-development
description: Creates specs before coding.
---

# Spec-Driven Development

Write a structured specification before writing any code.

## Gated Workflow: SPECIFY → PLAN → TASKS → IMPLEMENT (each phase reviewed by human)

## Spec Covers: Objective, Commands, Project Structure, Code Style, Testing Strategy, Boundaries (Always/Ask First/Never)

## Boundaries: Always (run tests, follow conventions, validate inputs), Ask First (DB schema changes, new deps, CI config), Never (commit secrets, edit vendor dirs, remove tests)

## Reframe instructions as success criteria: "Make dashboard faster" → "LCP < 2.5s on 4G, data load < 500ms, CLS < 0.1"

## Keep spec alive: Update when decisions/scope change, commit spec, reference in PRs