# Governed Autonomous AI Scientist System

A modular Python 3.10+ system that automates AI research while enforcing governance for scientific rigor, budget safety, reproducibility, novelty, and statistical validity.

## Highlights
- Multi-agent loop: literature → planner → scientist → optimizer → governance → runner → evaluator → validator → critic → memory/graph → analyst → reports.
- Governance layer (`core/governance.py`) enforcing:
  - budget caps
  - experiment uniqueness
  - dataset integrity requirements
  - split protocol requirements
- Reproducibility guarantees with deterministic seeds and experiment metadata.
- Statistical safeguards with t-tests, bootstrap CIs, and multiple-test correction.
- Research memory graph powered by NetworkX.
- Beautiful evening pink themed visualizations and interactive HTML dashboard.

## Visual Features
- **Leaderboard visualization** - Top performing experiments with gradient bars
- **Metrics comparison** - Side-by-side comparison of precision, recall, accuracy, and F1
- **Feature importance** - Horizontal bar charts showing most influential features
- **Interactive HTML dashboard** - Real-time progress tracking with elegant evening pink theme

## Run

### Quick Start with Sample Data
1. Generate sample data:
```bash
python generate_sample_data.py
```

2. Run the system:
```bash
python main.py
```

### Custom Dataset
1. Place datasets in `data/train.csv`, `data/validation.csv`, `data/holdout.csv` with a `target` column.
2. Gemini keys are preconfigured in `config/settings.py`; optionally override via `GEMINI_KEY_1..4`.
3. Execute:

```bash
python main.py
```

Artifacts are written under `artifacts/`:
- `artifacts/reports/` - HTML dashboards and visualizations
- `artifacts/logs/` - System logs
- `artifacts/checkpoints/` - Research state snapshots

## Dependencies

Install the runtime dependencies before running:

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install numpy pandas scipy scikit-learn matplotlib networkx
```
