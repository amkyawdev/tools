---
name: code-review-and-quality
description: Conducts multi-axis code review. Use before merging any change.
---

# Code Review and Quality

## Overview

Multi-dimensional code review with quality gates. Review covers five axes: correctness, readability, architecture, security, and performance.

## The Five-Axis Review

### 1. Correctness
Does the code do what it claims to do? Edge cases handled? Error paths covered?

### 2. Readability & Simplicity
Can another engineer understand this without explanation? Names descriptive? Control flow straightforward?

### 3. Architecture
Does the change fit the system's design? Follow existing patterns? Clean module boundaries?

### 4. Security
Is user input validated? Secrets out of code? Auth checks in place?

### 5. Performance
Any N+1 queries? Unbounded loops? Unnecessary re-renders?

## Change Sizing

Target ~100 lines per commit/PR. Changes over ~1000 lines should be split.

## Review Process

1. Understand the context
2. Review tests first
3. Review implementation across five axes
4. Categorize findings (Critical / Required / Nit / Optional)
5. Verify the verification story
