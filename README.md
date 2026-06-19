# okf-claude

> **Status: v0.1, testing-grade, public.** A thin kit that makes the memory you *already* have —
> git history, a Claude `memory/` bundle, and your skills — readable and writable as a single,
> portable [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
> (OKF) bundle, plus the skills that teach an agent how to **search** and **consolidate** that memory.

## Why this exists

Most agent "memory systems" reinvent a store. You don't need one. If you already run:

- **git** as the episodic log (what changed, when, why, what you rejected),
- a **`memory/` + `MEMORY.md`** bundle as durable facts (one fact per file, with frontmatter), and
- **skills** as procedural memory,

then you are already running the pattern OKF standardizes — markdown files + YAML frontmatter + an
index + a change log. OKF just pins down the small set of conventions that make it portable and
agent-queryable. **Adopting it is mostly a frontmatter rename + two generators.** This kit is those
generators and the skills that operate the result.

It also rides OKF for *optionality*: if the format gets non-Google adoption, your stack already
speaks it; if it doesn't, you've lost nothing — it's still just markdown in git.

## What's in the box

```
bin/okf-log        # generate log.md   <- FROM git history (section 7). Git is the source of truth.
bin/okf-index      # generate index.md <- FROM scanning a dir (section 6, progressive disclosure).
bin/okf-validate   # check a bundle for OKF v0.1 conformance (section 9).
skills/
  memory-search/      SKILL.md   # the read path: index-first, JIT, git recipes, freshness.
  memory-consolidate/ SKILL.md   # the out-of-band "dreaming" pass: merge, age-out, cap, human-gate.
viz/               # (vendored) Google's single-file OKF graph visualizer.
examples/sample-bundle/   # a tiny conformant bundle to test against.
```

All scripts are **Python 3 stdlib only** — no pip installs, no server, no API keys.

## Quick start

```sh
# Validate the sample bundle
bin/okf-validate examples/sample-bundle

# Regenerate the index for a memory directory (bundle root gets okf_version)
bin/okf-index examples/sample-bundle/facts

# Render git history as an OKF log.md (run inside any git repo)
bin/okf-log -o /tmp/log.md
```

To OKF-ify a real Claude `memory/` bundle: rename `metadata.type` -> top-level `type`, run
`okf-index` to (re)build `index.md`, run `okf-log` to emit `log.md` from git, then `okf-validate`.

## Design principles (learned from codegraph and other reputed repos)

We did not fork [codegraph](https://github.com/colbymchenry/codegraph) — we copied its *engineering
discipline*. codegraph wins on code-structure memory by being lean, local, single-source-of-truth,
and progressive-disclosure; those lessons transfer directly to *knowledge* memory:

| Lesson (codegraph et al.) | How okf-claude applies it |
|---|---|
| Expose the fewest high-leverage entry points (4 tools; one answers most in a single call). | `memory-search` is **one read path**, not a tool menu. |
| One tuned file is the single source of truth for agent behavior. | Each `SKILL.md` is the sole source of truth for its operation. |
| Local, zero-config, no server, no API keys; data is just committable files. | Bundle = markdown + git; scripts are **stdlib-only**. |
| Return the relevant slice + relationships, never the whole repo. | **Index-first + JIT**; "don't load the whole tree" is in the search bar. |
| Auto-sync + explicit staleness signals. | `log.md` / `index.md` are **generated, never hand-edited**; freshness-check + age-out. |
| Blast radius before changing a node. | Consolidate checks inbound links before retiring a concept. |
| Tune the surface against an observable metric. | Each skill carries an **observable bar + self-check**. |

## OKF conformance (v0.1, section 9)

A bundle is conformant when: every non-reserved `.md` has parseable YAML frontmatter; every
frontmatter block has a non-empty `type`; and reserved files (`index.md`, `log.md`) follow their
structure. Consumers must tolerate missing optional fields, unknown types/keys, broken links, and
missing `index.md`. `bin/okf-validate` enforces exactly this.

## License

MIT (intended). Not affiliated with Google; OKF is an open spec published by Google Cloud.
