---
name: performance-optimization
description: Optimizes application performance.
---

# Performance Optimization

Measure before optimizing. Profile first, identify bottleneck, fix, measure again.

## Core Web Vitals: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1

## Workflow: Measure → Identify → Fix → Verify → Guard

## Common Fixes
- N+1 queries → joins/includes
- Unbounded fetching → pagination
- Missing image optimization → srcset, lazy loading, AVIF/WebP
- Unnecessary re-renders → React.memo, useMemo, stable references
- Large bundle → code splitting, dynamic imports
- Missing caching → HTTP cache headers, in-memory cache

## Performance Budget: JS < 200KB gzipped, CSS < 50KB, Images < 200KB, API < 200ms p95