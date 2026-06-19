---
name: memory-consolidate
description: The out-of-band "dreaming" pass that keeps the OKF memory bundle small, fresh, and non-contradictory. Run on a schedule, at session spin-down, or just before compaction - NEVER on the hot path of an active task. Triggers on "consolidate memory", "the index is getting long", "memory feels stale", "dream", end-of-session cleanup.
---

# memory-consolidate - keep memory small, fresh, and true (run OUT of band)

Run this when you are NOT mid-task. Consolidation on the hot path adds latency and biases toward the current task. The goal is **fewer, better, current** memories - not more.

## Procedure
1. **Gather signal from FAILURES, not successes.** Read recent transcripts/commits for *recurring mistakes* and *contradictions*. Reflecting on wins induces reward hacking and over-fitted rules.
2. **Merge duplicates.** Two concepts saying the same thing -> one. Keep the version that carries the reason ("facts without reasoning decay; reasoning compounds").
3. **Age out stale.** A concept contradicted by current code, or superseded, is removed (its history stays in git). Refresh `timestamp` on the ones you keep.
4. **Enforce the caps.** `index.md` stays small (~200 lines / 25 KB - the bottom silently truncates past that). If adding would exceed the cap, evict the lowest-value concept first.
5. **Check inbound links before retiring a concept** (blast radius): `grep -rl '<concept-filename>' memory/`. Don't orphan cross-references - repoint or keep.
6. **Regenerate the derived views with the scripts, never by hand:**
   `bin/okf-index memory/ --okf-version 0.1` and `bin/okf-log -o memory/log.md`
7. **Validate, then gate.** Run `bin/okf-validate memory/`. Then PRESENT proposed deletions/merges to the human for approval before committing - autonomy without curation measurably degrades a memory/skill library (LLM-only curation ~ +0pp vs +16pp human-curated).

## The exclusion list (the rot-killer - never store these as concepts)
- Anything recoverable from `git log` / `git blame` (a dated change record - that's what `log.md` and trailers are for).
- In-progress task state (that belongs in a status file, not memory).
- A one-off instance instead of a generalizing rule.
- Anything a competent dev deduces from the code in ~5 seconds.

> Most memory bloat is an exclusion-list violation, not a length problem.

## The bar (good vs minimal)
- **GOOD:** net concept count and index size go DOWN or hold; every kept concept is current and carries its reason; deletions were human-approved; the bundle still passes `okf-validate`.
- **MINIMAL (FAILS):** appends new memories without removing any; "consolidates" by summarizing wins; deletes without approval; leaves the index over cap.

## MUST NOT
- Do NOT run on the hot path of an active task.
- Do NOT delete concepts without the human approval gate.
- Do NOT write reward-hackable rules - assert observable behavior, never intent.

## Self-check
Confirm: index size did not grow; failures (not wins) drove the changes; deletions were approved; `okf-validate` passes. If any is "no", fix before committing.
