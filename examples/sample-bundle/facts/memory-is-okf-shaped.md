---
type: reference
title: Our memory is already OKF-shaped
description: The Claude memory/ + MEMORY.md layout maps onto OKF.
resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
tags: [okf, memory, architecture]
timestamp: 2026-06-19T00:00:00Z
---
# Mapping
- OKF concept file   = memory/*.md (one fact per file)
- OKF required `type` = our metadata.type
- OKF index.md       = MEMORY.md
- OKF log.md         = git history (generated, never hand-written)

# So
Adopting OKF for ourselves is mostly a frontmatter rename plus index.md / log.md generators.
See [Use Context7 for libraries](use-context7-for-libs.md) for an unrelated example concept.
