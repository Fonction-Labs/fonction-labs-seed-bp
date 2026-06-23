from __future__ import annotations
import shutil
from pathlib import Path

from fonction_bp.config import Paths


def run(paths: Paths, scenario: str = "vc_case") -> Path:
    """Write dashboard files from root assets to dashboard/ output directory."""
    root = paths.root
    dash = paths.dashboard_dir

    dash.mkdir(parents=True, exist_ok=True)
    (dash / "assets").mkdir(parents=True, exist_ok=True)

    for filename in ("index.html",):
        shutil.copy2(root / filename, dash / filename)

    for filename in ("style.css", "dashboard.js"):
        src = root / "assets" / filename
        if src.exists():
            shutil.copy2(src, dash / "assets" / filename)

    if paths.dashboard_data_js.exists():
        shutil.copy2(paths.dashboard_data_js, root / "assets" / "dashboard_data.js")

    return dash / "index.html"
