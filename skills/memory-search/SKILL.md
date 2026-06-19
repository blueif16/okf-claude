---
name: memory-search
description: Recall the right past decision, fact, or reason from the OKF memory bundle + git history BEFORE acting. Use when about to make a decision that may already be settled, when you need the reason behind an existing choice, when an error may have a known fix, or when starting work in an unfamiliar area. Triggers on "have we decided", "why is X this way", "did we hit this before", "what's our convention for".
---

# memory-search - read the memory, don't re-derive it

Memory here is an **OKF bundle** (`memory/*.md` concept files + an `index.md`) **plus git history** (the episodic log; `log.md` is its generated view). Your job: retrieve the **smallest correct slice and stop**. Loading everything is the failure mode, not the goal - accuracy drops sharply past ~32K tokens of loaded context.

## Read path (in order - stop as soon as you have the answer)
1. **Index first.** Read `index.md` - the cheap map (titles + one-line descriptions grouped by `type`). Pick the 1-3 concepts that match. NEVER walk the whole tree first.
2. **Open only those concepts.** Read the matched concept file(s) in full. Each is one fact/decision.
3. **Ask git for the "why" and the history** before re-deciding anything (recipes below).
4. **Check freshness.** If a concept's `timestamp` is old or the area changed since, treat it as a point-in-time observation, not live state - verify against current code before trusting.

## Git retrieval recipes (the episodic read path)
- Why a decision/area is the way it is: `git log --grep '<keyword>' --all-match`
- Evolution of one subsystem, newest first, with the lesson inline:
  `git log --grep '^skillsys(<owner>)' --pretty=format:'%h %ad %s%n  - %(trailers:key=Lesson,valueonly=true)' --date=short`
- What was already TRIED and REJECTED here (read BEFORE re-proposing):
  `git log --grep '<owner>' --pretty='%h %s%n%(trailers:key=Rejected,valueonly=true)'`
- When/why a symbol or rule entered: `git log -S '<symbol>' -p`
- History of one block: `git log -L '/<start-marker>/,/<end-marker>/:<file>'`
- Why a file/dir changed at all: `git log --pretty='%h %s' -- <path>`

## The bar (good vs minimal)
- **GOOD:** you cite the specific concept file and/or commit SHA your answer rests on; you checked the `Rejected:` trail before proposing something that may have already failed; you loaded <= 3 concepts.
- **MINIMAL (FAILS):** answering from prior knowledge without checking memory; or loading the entire `memory/` tree "to be safe."

## MUST NOT
- Do NOT re-decide something `git log --grep` shows was already decided or rejected.
- Do NOT load concepts you don't need, or paste whole files when one line answers it.
- Do NOT trust a stale entry over the current code - freshness-check first.

## Self-check before acting
Confirm: (1) I read `index.md` before opening concepts. (2) I can name the concept and/or SHA backing my answer. (3) I checked the `Rejected:` trail if I'm about to propose a change. If any is "no", do that step before proceeding.
