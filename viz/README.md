# viz/ — OKF graph visualizer

Renders an OKF bundle as an interactive force-directed graph in a **single
HTML file** (no backend; the bundle data is embedded in the page). This is
**Google's reference OKF visualizer, vendored verbatim** — not a
re-implementation. See [`PROVENANCE.md`](PROVENANCE.md) for the source repo,
commit SHA, and the exact file mapping. License: Apache-2.0 (Google) —
[`LICENSE.md`](LICENSE.md).

## Regenerate

`regen.py` is a thin wrapper that runs Google's vendored generator standalone.
Its only runtime dependency is PyYAML (no `google-adk` / BigQuery install).

```sh
python3 -m venv /tmp/okf-venv
/tmp/okf-venv/bin/pip install pyyaml
/tmp/okf-venv/bin/python viz/regen.py \
    --bundle <bundle-dir> \
    --out    <bundle-dir>/graph.html \
    --name   "<display name>"
# default --out is <bundle>/viz.html, matching Google's CLI
```

Then open the produced HTML in a browser.

The wrapper calls Google's `generate_visualization` unchanged and produces
byte-identical output to upstream's `python -m enrichment_agent visualize`.
To run the *upstream* CLI instead, clone
[knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog),
`pip install -e okf/`, and run `python -m enrichment_agent visualize --bundle …`.

## What it shows

- A force-directed graph of every concept (one node per non-`index.md`
  markdown file), colored by `type`, with directed edges drawn from each
  intra-bundle markdown link.
- A detail panel per concept (frontmatter + rendered markdown body), a
  "Cited by" backlinks list, a search box, a type filter, and switchable
  layouts.

## Caveats (verified against this repo's bundles)

- **CDN at runtime.** The HTML embeds all bundle *data*, but the template
  loads two JS libraries from a CDN when opened — `cytoscape@3.28.1` and
  `marked@12.0.0` from `cdn.jsdelivr.net`. It is self-contained for data but
  needs network access to render. (Upstream design.)
- **Edge detection expects *relative* links.** Google's link extractor skips
  any markdown link target that is absolute (starts with `/`) or external.
  A bundle that writes intra-bundle links as `/okf/foo.md` will
  render all its nodes but **zero edges**; only relative links like
  `subsystems/foo.md` produce edges. `index.md` is excluded from the graph,
  so relative links living only there do not count.
