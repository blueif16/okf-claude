# Provenance

The OKF graph visualizer in this directory is **copied verbatim from Google's
reference implementation** of the Open Knowledge Format (OKF).

- **Source repo:** <https://github.com/GoogleCloudPlatform/knowledge-catalog>
- **Path in repo:** `okf/src/enrichment_agent/viewer/` (plus the one intra-repo
  dependency `okf/src/enrichment_agent/bundle/document.py`)
- **Commit SHA:** `d2b9e2e13ccb2528af555b207b3c73312757b7c5`
- **License:** Apache-2.0 (Copyright Google LLC). Full text in `LICENSE.md`.

## What is vendored verbatim (Google's code, unmodified)

| File here                     | Source in knowledge-catalog                                  |
|-------------------------------|--------------------------------------------------------------|
| `viewer/generator.py`         | `okf/src/enrichment_agent/viewer/generator.py`               |
| `viewer/__init__.py`          | `okf/src/enrichment_agent/viewer/__init__.py`                |
| `viewer/templates/viz.html`   | `okf/src/enrichment_agent/viewer/templates/viz.html`         |
| `viewer/static/viz.css`       | `okf/src/enrichment_agent/viewer/static/viz.css`             |
| `viewer/static/viz.js`        | `okf/src/enrichment_agent/viewer/static/viz.js`              |
| `bundle/document.py`          | `okf/src/enrichment_agent/bundle/document.py`                |
| `LICENSE.md`                  | `okf/LICENSE.md`                                             |

These files are byte-for-byte copies. Do not edit them; re-vendor from the
upstream commit instead.

## What is local to okf-claude (NOT Google's)

- `regen.py` — a thin wrapper that registers the vendored modules under the
  `enrichment_agent.*` import names Google's verbatim `generator.py` expects,
  so the visualizer runs standalone with PyYAML as the only dependency (no
  `google-adk` / BigQuery install needed). It calls Google's
  `generate_visualization` unchanged.
- `bundle/__init__.py`, `viewer` package markers as needed for import.
- `README.md`, this `PROVENANCE.md`.

## Note on "self-contained"

The generated HTML embeds the entire bundle as a JSON blob (no backend; data
never leaves the page). However, the template loads two JS libraries from a
CDN at runtime — `cytoscape@3.28.1` and `marked@12.0.0` from
`cdn.jsdelivr.net`. It is therefore self-contained for *data* but requires
network access to fetch those two libraries when opened. This matches the
upstream design.
