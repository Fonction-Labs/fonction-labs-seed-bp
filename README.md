# Fonction Labs BP Pipeline v2

Reproducible financial model pipeline for the Fonction Labs seed BP.

This version is designed to avoid the V4 / V5 / V6 divergence issue:

- raw data and assumptions are inputs;
- DuckDB tables are the single source of truth;
- the full BP Excel, simplified BP Excel and dashboard are outputs;
- validation checks that key KPIs align across outputs.

## Quick start

```bash
uv sync --default-index https://pypi.org/simple
uv run python -m fonction_bp.pipeline build --scenario vc_case
```

If you do not use uv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install duckdb openpyxl pyyaml
PYTHONPATH=src python3 -m fonction_bp.pipeline build --scenario vc_case
```

## Outputs

After running the pipeline:

```text
outputs / data/processed/model.duckdb                         # model database
data/processed/model_outputs.json                             # structured model output
data/processed/validation_report.json                         # automated checks
downloads/Fonction_Labs_BP_Seed_2026_2028_full_pipeline_v2.xlsx
downloads/Fonction_Labs_BP_Seed_2026_2028_simplified_pipeline_v2.xlsx
index.html                                                    # dashboard copy at repo root
dashboard/index.html                                          # dashboard source
```

## Core command

```bash
uv run python -m fonction_bp.pipeline build --scenario vc_case
```

Pipeline order:

1. `ingest_raw`: parse Qonto archive and Attio funnel extract.
2. `load_assumptions`: load `data/assumptions/vc_case.yaml` into DuckDB.
3. `compute_model`: compute cohort, revenue, ARR, FDE capacity, headcount, opex and cash tables.
4. `build_model_outputs`: export structured JSON / JS dashboard data.
5. `export_full_excel`: generate the full BP workbook.
6. `export_simplified_excel`: generate the VC-facing simplified workbook.
7. `export_dashboard`: generate the static HTML dashboard.
8. `validate`: run consistency checks.

## Chat assistant

A conversational interface to the BP model, running alongside the dashboard.

```bash
cd chat
./setup.sh          # install deps, symlink data/processed and docs/
npm run dev         # backend :8002 + frontend :3000
```

Open `http://localhost:3000` — dashboard on the left, chat on the right.

The agent has access to:
- **DuckDB** (`data/processed/model.duckdb`) — mandatory for all numerical questions
- **Markdown context** (`docs/`, `CONTEXT_FOR_LLM.md`, `AGENT.md`) — for strategy/narrative questions
- **Assumptions** (`data/assumptions/vc_case.yaml`)

Requires `OPENAI_API_KEY` in `chat/backend/.env`.

## Important rule

Do not edit generated Excel outputs manually. Update raw files or assumptions, then rerun the pipeline.

## Dashboard polish update

This package uses the pipeline v2 model as the single source of truth, but the HTML dashboard has been restored to a fuller, more polished dashboard-only layout:

- hero + six KPI cards;
- three-year trajectory cards;
- 2026 monthly revenue view;
- enterprise revenue model table;
- accounts / use cases milestone view;
- revenue mix and ARR build-up;
- FDE capacity, cash runway and use-of-funds;
- downloads for both Excel workbooks.

The dashboard reads `assets/dashboard_data.js`, which is generated from `data/processed/model_outputs.json` / DuckDB tables. It should not contain hardcoded financial figures beyond the structure and narrative copy.
