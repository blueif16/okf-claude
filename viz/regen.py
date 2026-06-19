#!/usr/bin/env python3
"""Regenerate an OKF bundle's self-contained HTML graph.

Thin wrapper around Google's vendored OKF visualizer (see PROVENANCE.md).
Google's `generator.py` is kept VERBATIM and still does
`from enrichment_agent.bundle.document import OKFDocument`; this wrapper
registers the vendored modules under that namespace so the visualizer runs
standalone (only dependency: PyYAML) without installing the full
enrichment-agent / google-adk stack.

Usage:
    python3 viz/regen.py --bundle <bundle-dir> [--out <out.html>] [--name <name>]

Output defaults to <bundle>/viz.html, matching Google's CLI.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import types
from pathlib import Path

_VIZ_ROOT = Path(__file__).resolve().parent


def _load(mod_name: str, file_path: Path) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(mod_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {mod_name} from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


def _wire_namespace() -> None:
    """Map vendored files onto the `enrichment_agent.*` import paths that
    Google's verbatim source expects."""
    for pkg in ("enrichment_agent", "enrichment_agent.bundle",
                "enrichment_agent.viewer"):
        if pkg not in sys.modules:
            sys.modules[pkg] = types.ModuleType(pkg)
    _load("enrichment_agent.bundle.document",
          _VIZ_ROOT / "bundle" / "document.py")
    _load("enrichment_agent.viewer.generator",
          _VIZ_ROOT / "viewer" / "generator.py")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bundle", required=True, type=Path,
                   help="Path to the bundle root directory.")
    p.add_argument("--out", type=Path, default=None,
                   help="Output HTML path (default: <bundle>/viz.html).")
    p.add_argument("--name", default=None,
                   help="Display name (default: bundle directory name).")
    args = p.parse_args(argv)

    _wire_namespace()
    from enrichment_agent.viewer.generator import generate_visualization

    out = args.out or (args.bundle / "viz.html")
    stats = generate_visualization(args.bundle, out, bundle_name=args.name)
    print(
        f"Wrote {stats['concepts']} concept(s), "
        f"{stats['edges']} edge(s), "
        f"{stats['bytes']} bytes -> {out}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
