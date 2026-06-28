"""Tool: read markdown context files for business plan information."""

from __future__ import annotations

import json
from pathlib import Path

from agents import RunContextWrapper, function_tool

from app.agents.bp_agent import BPAgentContext

PROJECT_ROOT = Path(__file__).resolve().parents[4]

ALLOWED_FILES = {
    "CONTEXT_FOR_LLM": PROJECT_ROOT / "CONTEXT_FOR_LLM.md",
    "AGENT": PROJECT_ROOT / "AGENT.md",
    "T1.1_narrative": PROJECT_ROOT / "docs" / "T1.1_narrative-3-etapes_conclusions.md",
    "T1.2_modeles": PROJECT_ROOT / "docs" / "T1.2_modeles-intermediaire-vs-cible_conclusions.md",
    "T1.3_arr": PROJECT_ROOT / "docs" / "T1.3_arr-decomposition_conclusions.md",
    "T2_synthese": PROJECT_ROOT / "docs" / "T2_synthese-complete_conclusions.md",
    "T3_depenses": PROJECT_ROOT / "docs" / "T3_depenses-headcount_conclusions.md",
    "T4_strategie": PROJECT_ROOT / "docs" / "T4_strategie-enterprise_conclusions.md",
}


@function_tool(description_override=(
    "Read a business plan context document. Available files: "
    "CONTEXT_FOR_LLM (overview & key metrics), "
    "AGENT (model rules & formulas), "
    "T1.1_narrative (3-stage evolution narrative), "
    "T1.2_modeles (intermediate vs target model), "
    "T1.3_arr (ARR decomposition by cohort), "
    "T2_synthese (complete synthesis), "
    "T3_depenses (headcount & expenses strategy), "
    "T4_strategie (enterprise strategy)."
))
async def read_context(ctx: RunContextWrapper[BPAgentContext], file_key: str) -> str:
    if file_key not in ALLOWED_FILES:
        return json.dumps({"error": f"Unknown file_key '{file_key}'. Available: {list(ALLOWED_FILES.keys())}"})
    path = ALLOWED_FILES[file_key]
    if not path.exists():
        return json.dumps({"error": f"File not found: {path}"})
    return json.dumps({"file": file_key, "content": path.read_text(encoding="utf-8")}, ensure_ascii=False)
