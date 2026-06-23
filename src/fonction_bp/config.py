from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Paths:
    root: Path
    raw_qonto_dir: Path
    raw_attio_dir: Path
    assumptions_dir: Path
    processed_dir: Path
    outputs_dir: Path
    downloads_dir: Path
    dashboard_dir: Path
    duckdb_path: Path
    model_outputs_json: Path
    dashboard_data_js: Path

    @classmethod
    def from_root(cls, root: Path) -> "Paths":
        root = root.resolve()
        return cls(
            root=root,
            raw_qonto_dir=root / "data" / "raw" / "qonto",
            raw_attio_dir=root / "data" / "raw" / "attio",
            assumptions_dir=root / "data" / "assumptions",
            processed_dir=root / "data" / "processed",
            outputs_dir=root / "outputs",
            downloads_dir=root / "downloads",
            dashboard_dir=root / "dashboard",
            duckdb_path=root / "data" / "processed" / "model.duckdb",
            model_outputs_json=root / "data" / "processed" / "model_outputs.json",
            dashboard_data_js=root / "dashboard" / "assets" / "dashboard_data.js",
        )

    def ensure_dirs(self) -> None:
        for path in [self.processed_dir, self.outputs_dir, self.downloads_dir, self.dashboard_dir / "assets"]:
            path.mkdir(parents=True, exist_ok=True)
