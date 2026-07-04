---
name: deprecation-and-migration
description: Manages deprecation and migration.
---
# Deprecation and Migration

Code is a liability. Every line has ongoing cost.

Core: Hyrum's Law makes removal hard. Plan deprecation at design time. Advisory vs Compulsory.

Migration: 1.Build replacement 2.Announce+document 3.Migrate incrementally 4.Remove old system.
Patterns: Strangler (parallel), Adapter (translate), Feature Flag (per user).
Zombie Code: unmaintained + active consumers → assign owner or deprecate.