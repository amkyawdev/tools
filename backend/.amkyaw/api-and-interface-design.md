---
name: api-and-interface-design
description: Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface.
---

# API and Interface Design

## Overview

Design stable, well-documented interfaces that are hard to misuse. Good interfaces make the right thing easy and the wrong thing hard.

## When to Use

- Designing new API endpoints
- Defining module boundaries or contracts between teams
- Creating component prop interfaces

## Core Principles

### Hyrum's Law

> With a sufficient number of users of an API, all observable behaviors of your system will be depended on by somebody.

### Contract First

Define the interface before implementing it. The contract is the spec — implementation follows.

### Consistent Error Semantics

Pick one error strategy and use it everywhere.

### Validate at Boundaries

Trust internal code. Validate at system edges where external input enters.

## REST API Patterns

Use plural nouns, pagination on list endpoints, PATCH for partial updates.

## TypeScript Interface Patterns

Use discriminated unions, input/output separation, branded types for IDs.
