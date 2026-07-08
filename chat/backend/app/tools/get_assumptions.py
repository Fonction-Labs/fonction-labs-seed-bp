"""Tool: read and return the vc_case.yaml assumptions."""

from __future__ import annotations

import json
from pathlib import Path

import os

import yaml
from agents import RunContextWrapper, function_tool

from app.agents.bp_agent import BPAgentContext


def _resolve_assumptions_path() -> Path:
    env = os.getenv("ASSUMPTIONS_PATH")
    if env:
        return Path(env)
    parts = Path(__file__).resolve().parts
    repo_root = Path(*parts[: len(parts) - 4])
    return repo_root / "data" / "assumptions" / "vc_case.yaml"

ASSUMPTIONS_PATH = _resolve_assumptions_path()


@function_tool(description_override=(
    "Return the master assumptions from vc_case.yaml — pricing, cohort plan, "
    "headcount, FDE parameters, use of funds, and all model parameters."
))
async def get_assumptions(ctx: RunContextWrapper[BPAgentContext]) -> str:
    if not ASSUMPTIONS_PATH.exists():
        return json.dumps({"error": f"Assumptions file not found: {ASSUMPTIONS_PATH}"})
    try:
        with open(ASSUMPTIONS_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return json.dumps(data, ensure_ascii=False, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
