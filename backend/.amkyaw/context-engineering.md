---
name: context-engineering
description: Optimizes agent context setup. Use when starting a new session or when agent output quality degrades.
---

# Context Engineering

## Overview

Feed agents the right information at the right time. Context is the single biggest lever for agent output quality.

## The Context Hierarchy

1. **Rules Files** (CLAUDE.md, etc.) — Always loaded, project-wide
2. **Spec / Architecture Docs** — Loaded per feature/session
3. **Relevant Source Files** — Loaded per task
4. **Error Output / Test Results** — Loaded per iteration
5. **Conversation History** — Accumulates, compacts

## Context Packing Strategies

- **The Brain Dump**: Structured block at session start
- **The Selective Include**: Only what's relevant to current task
- **The Hierarchical Summary**: Maintain a summary index for large projects

## Anti-Patterns

- Context starvation → Agent hallucinates
- Context flooding → Agent loses focus
- Stale context → Agent references outdated patterns
- Missing examples → Agent invents new style
