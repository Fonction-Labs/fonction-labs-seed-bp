from __future__ import annotations
import argparse
from pathlib import Path

from fonction_bp.config import Paths
from fonction_bp.steps import ingest_raw, load_assumptions, compute_model, build_model_outputs, export_full_excel, export_simplified_excel, export_dashboard, validate


def build(root: Path, scenario: str = "vc_case") -> None:
    paths = Paths.from_root(root)
    paths.ensure_dirs()
    print("[1/7] ingest_raw")
    ingest_raw.run(paths, scenario)
    print("[2/7] load_assumptions")
    load_assumptions.run(paths, scenario)
    print("[3/7] compute_model")
    compute_model.run(paths, scenario)
    print("[4/7] build_model_outputs")
    build_model_outputs.run(paths, scenario)
    print("[5/7] export_excel")
    full_path = export_full_excel.run(paths, scenario)
    simple_path = export_simplified_excel.run(paths, scenario)
    print(f"      full: {full_path}")
    print(f"      simplified: {simple_path}")
    print("[6/7] export_dashboard")
    dashboard = export_dashboard.run(paths, scenario)
    print(f"      dashboard: {dashboard}")
    print("[7/7] validate")
    report = validate.run(paths, scenario)
    print(f"      validation: {report}")
    print("Pipeline complete.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Fonction Labs BP pipeline outputs.")
    sub = parser.add_subparsers(dest="command")
    build_parser = sub.add_parser("build")
    build_parser.add_argument("--scenario", default="vc_case")
    build_parser.add_argument("--root", default=".")
    args = parser.parse_args()
    if args.command == "build":
        build(Path(args.root), args.scenario)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
