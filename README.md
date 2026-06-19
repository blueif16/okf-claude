# okf-claude

**A four-layer knowledge architecture for coding agents** — give an agent the *right* knowledge at the *right* altitude (code structure · change history · durable meaning · the loop that maintains them), using formats you mostly already have, unified behind the [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) (OKF).

> **Status: v0.1 — actively dogfooded** on a real, actively-developed skill-system codebase to measure whether it earns its keep. This README and [`DESIGN.md`](DESIGN.md) stay honest about what's *proven* vs. *promising*.

## The idea in one breath

Agents rarely fail for lack of a database. They fail from **context rot** — drowning in the *wrong* context. (Measured: model accuracy falls from ~90% to ~51% as a conversation grows; many models drop below 50% past ~32K tokens.) The fix is not a bigger store. It is **four thin layers, each the single source of truth for one kind of knowledge, each *linking* to the others instead of *copying* them:**

| Layer | Answers the question | Lives in | Derivable? | Freshness |
|---|---|---|---|---|
| **① Structural** (codegraph) | *what calls what · blast radius · where defined* | local SQLite, built from the AST | yes — mechanical | auto-synced |
| **② Episodic** (git) | *what changed · when · why · what we rejected* | commit messages + trailers | it **is** the source of truth | append-only |
| **③ Semantic** (OKF concepts) | *why · the invariant · who owns this · the lesson* | markdown + YAML frontmatter | **no** — must be curated | slow-changing |
| **④ Procedural** ([Hermes skills](https://github.com/blueif16/hermes-skill-system)) | *the loop that keeps the other three true* | `SKILL.md` | authored | human-gated |

Layers ① and ② you largely **already have**. Layer ③ is the one the others *structurally cannot produce*. Layer ④ is why it doesn't rot.

The payoff: **the highest-level understanding of a system for the lowest reading effort** — open one `index.md` and a few concept docs instead of grepping tens of thousands of lines.

→ The full philosophy, the role of each layer, why git-as-memory and codegraph are genuinely innovative, the design guidelines from the research, and the diagrams live in **[`DESIGN.md`](DESIGN.md)**.

## What's in the box (the tooling)

```
bin/okf-validate   # OKF v0.1 conformance check (spec §9)
bin/okf-index      # generate index.md  (progressive disclosure, §6) — from a directory
bin/okf-log        # generate log.md    (§7) — rendered FROM git history, e.g. --grep '^skillsys'
bin/okf-graph      # zero-dependency, fully-offline force-graph visualizer (no CDN, no deps)
viz/               # Google's reference OKF visualizer, vendored verbatim (Apache-2.0; see PROVENANCE)
skills/            # memory-search + memory-consolidate — the read & consolidation discipline as agent skills
examples/          # a small conformant bundle to test against
```

All generators are **Python 3 stdlib only** — no pip installs, no server, no API keys, nothing leaves your machine.

## Quickstart

```sh
# validate a bundle
bin/okf-validate examples/sample-bundle

# (re)build the index for a knowledge directory
bin/okf-index examples/sample-bundle --recursive --okf-version 0.1

# render git history as an OKF change log (run inside any git repo)
bin/okf-log --grep '^skillsys' -o /tmp/log.md      # scope to a commit convention if you use one

# see it as a graph (offline, zero-dep)
bin/okf-graph examples/sample-bundle -o /tmp/graph.html && open /tmp/graph.html
```

To OKF-ify an existing markdown knowledge base: add a top-level `type:` to each file's frontmatter, run `okf-index` to build `index.md`, run `okf-log` to emit `log.md` from git, then `okf-validate`.

## What it is — and isn't (honest framing)

- **It is** a thin **format + tooling + discipline** layer over things you already keep (git, markdown files, skills), plus an *optional* deterministic code index. The value is **unification, portability, and the curation discipline** — not a new engine.
- **It isn't** a database, a vector store, an embedding pipeline, or a platform. OKF itself is young (v0.1) and is, by design, "just markdown + frontmatter" — it standardizes *structural* interoperability, not semantic meaning. We adopt it for portability and optionality, not because a format is magic.
- Each layer has places it **doesn't** help (codegraph adds nothing to prose knowledge; OKF adds no modeling power a catalog doesn't already have). `DESIGN.md` is explicit about those edges.

## License

MIT for this kit (see [`LICENSE`](LICENSE)). The vendored visualizer under [`viz/`](viz/) is **Google's** OKF reference implementation, **Apache-2.0** — see [`viz/LICENSE.md`](viz/LICENSE.md) and [`viz/PROVENANCE.md`](viz/PROVENANCE.md). Not affiliated with Google; OKF is an open spec published by Google Cloud.
