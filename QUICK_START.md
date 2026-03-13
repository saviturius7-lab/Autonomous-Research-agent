# Quick Start Guide - Evening Pink Visual Theme

## Installation

```bash
pip install -r requirements.txt
```

## Generate Sample Data

```bash
python3 generate_sample_data.py
```

This creates:
- `data/train.csv` (1000 samples)
- `data/validation.csv` (300 samples)
- `data/holdout.csv` (200 samples)

## Preview Visualizations

Before running the full system, preview the evening pink theme:

```bash
python3 preview_visuals.py
```

Results in `artifacts/preview/`:
- `sample_leaderboard.png`
- `sample_metrics.png`
- `sample_features.png`

## Run the System

```bash
python3 main.py
```

This generates (every iteration):
- `artifacts/reports/leaderboard_XXXX.png`
- `artifacts/reports/metrics_comparison_XXXX.png`
- `artifacts/reports/feature_importance_XXXX.png`
- `artifacts/reports/dashboard_XXXX.html`
- `artifacts/reports/report_XXXX.json`

## View Results

### Open Latest Dashboard
```bash
python3 view_dashboard.py
```

### Or Manually
```bash
open artifacts/reports/dashboard_0000.html
```

## What You'll See

### Dashboard Features
1. **Statistics Cards**
   - Total experiments
   - Experiments run (with progress bar)
   - API calls (with progress bar)
   - Runtime hours (with progress bar)

2. **Leaderboard Table**
   - Rank
   - Experiment ID
   - Model name
   - F1 Score
   - Validation status

3. **Visualizations**
   - Leaderboard bar chart
   - Metrics comparison
   - Feature importance

4. **Pattern Analysis**
   - Top features
   - Top models

### Visual Theme
- **Background**: Deep twilight purple
- **Primary**: Vibrant pink
- **Secondary**: Soft rose
- **Accent**: Warm cream

## File Structure

```
project/
├── ai_scientist_system/
│   └── reports/
│       ├── visualization.py          # Chart generation
│       ├── dashboard_generator.py    # HTML dashboards
│       └── theme_config.py           # Theme configuration
├── artifacts/
│   ├── reports/                      # Generated reports
│   ├── preview/                      # Preview samples
│   └── logs/                         # System logs
├── data/                             # Datasets
├── generate_sample_data.py           # Data generator
├── preview_visuals.py                # Preview tool
├── view_dashboard.py                 # Dashboard viewer
└── main.py                           # Main entry point
```

## Customization

### Change Colors
Edit `ai_scientist_system/reports/theme_config.py`:
```python
EVENING_PINK = {
    "background": "#2a1a2e",  # Your color
    "primary": "#e84393",     # Your color
    # ... etc
}
```

### Adjust Chart Size
In `visualization.py`:
```python
fig, ax = plt.subplots(figsize=(14, 7))  # Change dimensions
```

### Modify Dashboard Layout
Edit `dashboard_generator.py` HTML template

## Troubleshooting

### Module Not Found
```bash
pip install --break-system-packages -q matplotlib numpy pandas scipy scikit-learn networkx
```

### No Data
```bash
python3 generate_sample_data.py
```

### Empty Dashboard
Run at least one iteration:
```bash
python3 main.py
```

## Next Steps

1. Try with your own dataset (replace files in `data/`)
2. Adjust experiment parameters in `ai_scientist_system/config/settings.py`
3. Customize visual theme in `theme_config.py`
4. Add new visualization types in `visualization.py`

## Support

Check these files for more info:
- `README.md` - Full system documentation
- `VISUAL_ENHANCEMENTS.md` - Visual design details
- `CHANGES_SUMMARY.md` - Complete changelog
