---
name: code-simplification
description: Simplifies code for clarity. Use when refactoring code for clarity without changing behavior.
---

# Code Simplification

## Overview

Simplify code by reducing complexity while preserving exact behavior. The goal is code that is easier to read, understand, modify, and debug.

## The Five Principles

### 1. Preserve Behavior Exactly
Don't change what the code does — only how it expresses it.

### 2. Follow Project Conventions
Simplification means making code more consistent with the codebase.

### 3. Prefer Clarity Over Cleverness
Explicit code is better than compact code when the compact version requires a mental pause.

### 4. Maintain Balance
Don't over-simplify — inlining too aggressively or combining unrelated logic.

### 5. Scope to What Changed
Default to simplifying recently modified code. Avoid drive-by refactors.

## The Simplification Process

1. Understand before touching (Chesterton's Fence)
2. Identify simplification opportunities
3. Apply changes incrementally
4. Verify the result
