---
name: test-driven-development
description: Drives development with tests.
---

# Test-Driven Development

Write a failing test before writing the code that makes it pass. For bug fixes, reproduce the bug with a test before fixing.

## TDD Cycle: RED (write failing test) → GREEN (minimal code to pass) → REFACTOR (clean up while tests green)

## Prove-It Pattern (Bug Fixes): Write reproduction test → confirm it fails → implement fix → test passes → full suite

## Test Pyramid: ~80% Unit (pure logic, ms), ~15% Integration (boundaries, seconds), ~5% E2E (critical flows, minutes)

## Good Tests: Test state not interactions, DAMP over DRY, Arrange-Act-Assert, one assertion per concept, descriptive names

## Anti-Patterns: Testing implementation details, flaky tests, testing framework code, snapshot abuse, no test isolation