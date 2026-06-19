# viz/ — OKF graph visualizer

OKF bundles render as an interactive graph with a **single self-contained HTML file**
(no backend; the data stays on the page). Rather than re-implement it, vendor Google's
reference visualizer from the OKF repo:

```sh
# from the GoogleCloudPlatform/knowledge-catalog repo, under okf/
#   the `visualize` subcommand emits a single HTML file pointed at a bundle.
# Copy the produced HTML here as viz/index.html, then open it against a bundle:
#   bin/okf-validate examples/sample-bundle   # confirm conformance first
#   open viz/index.html                        # then load the bundle directory
```

Spec + reference impl: <https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf>

> Not vendored yet (kept honest — no fabricated file). This is the one optional
> piece remaining in v0.1; the three generators and two skills are complete and tested.
