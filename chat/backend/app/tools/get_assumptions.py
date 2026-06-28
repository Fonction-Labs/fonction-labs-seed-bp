"""Tool: read and return the vc_case.yaml assumptions."""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from agents import RunContextWrapper, function_tool

from app.agents.bp_agent import BPAgentContext

ASSUMPTIONS_PATH = Path(__file__).resolve().parents[4] / "data" / "assumptions" / "vc_case.yaml"


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
