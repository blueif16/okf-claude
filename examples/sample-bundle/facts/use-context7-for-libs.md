---
type: feedback
title: Use Context7 for libraries
description: Resolve library docs via Context7 before writing integration code.
tags: [tooling, libraries]
timestamp: 2026-06-19T00:00:00Z
---
# Rule
Before writing code against any external library or framework, resolve its docs via Context7 (resolve-library-id -> get-library-docs).

# Why
Training data lags releases; Context7 returns current APIs and avoids deprecated calls.
