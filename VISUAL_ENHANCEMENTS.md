# Visual Enhancements - Evening Pink Theme

This document outlines the visual improvements made to the AI Scientist System with an elegant evening pink theme.

## Color Palette

The evening pink theme uses a sophisticated color scheme:

- **Background**: `#2a1a2e` - Deep twilight purple
- **Surface**: `#3d2c45` - Rich plum surface
- **Primary**: `#e84393` - Vibrant pink
- **Secondary**: `#fd79a8` - Soft rose
- **Tertiary**: `#fab1a0` - Peach accent
- **Accent**: `#ffeaa7` - Warm cream
- **Text Primary**: `#ffffff` - Pure white
- **Text Secondary**: `#dfe6e9` - Light gray
- **Grid**: `#574b60` - Muted purple

## New Visualizations

### 1. Enhanced Leaderboard Plot
**Location**: `ai_scientist_system/reports/visualization.py`

Features:
- Gradient color bars from deep to light pink
- Value labels on top of each bar
- Clean, modern design with custom grid styling
- High-resolution output (300 DPI)
- Professional spacing and typography

### 2. Metrics Comparison Plot
**Location**: `ai_scientist_system/reports/visualization.py`

Features:
- Multi-metric comparison (accuracy, precision, recall, F1)
- Grouped bar chart with distinct colors per metric
- Color-coded legend with semi-transparent background
- Supports top N experiments comparison

### 3. Feature Importance Plot
**Location**: `ai_scientist_system/reports/visualization.py`

Features:
- Horizontal bar chart for easy reading
- Gradient colors showing importance ranking
- Precise value labels
- Sorted by importance descending

### 4. Interactive HTML Dashboard
**Location**: `ai_scientist_system/reports/dashboard_generator.py`

Features:
- Real-time experiment tracking
- Budget monitoring with progress bars
- Top performers leaderboard table
- Embedded visualizations
- Responsive design
- Pattern analysis display
- Hover effects and smooth transitions

## Dashboard Sections

### Header
- System title with gradient background
- Current iteration display
- Elegant border with pink accent

### Statistics Grid
- Total experiments count
- Experiments run with progress bar
- API calls tracking with progress bar
- Runtime hours monitoring with progress bar

### Leaderboard Table
- Rank, Experiment ID, Model, Score, Status
- Hover effects on rows
- Color-coded badges for validation status
- Monospace font for experiment IDs

### Visualizations Grid
- Three main visualizations side-by-side
- Responsive layout
- High-quality PNG embedding

### Patterns Section
- Top features list
- Top models list
- Two-column layout
- Styled list items with pink accent borders

## File Structure

```
ai_scientist_system/
├── reports/
│   ├── visualization.py          # Enhanced matplotlib plots
│   ├── dashboard_generator.py    # HTML dashboard generator
│   └── report_generator.py       # JSON reports
└── main.py                        # Updated to use new visuals

artifacts/
└── reports/
    ├── leaderboard_XXXX.png
    ├── metrics_comparison_XXXX.png
    ├── feature_importance_XXXX.png
    └── dashboard_XXXX.html
```

## Usage

### Generate Preview Visuals
```bash
python3 preview_visuals.py
```

### Run Full System
```bash
python3 generate_sample_data.py  # Create sample datasets
python3 main.py                  # Run the system
```

### View Results
Open `artifacts/reports/dashboard_XXXX.html` in your browser to see:
- Live experiment tracking
- Beautiful visualizations
- Progress monitoring
- Pattern insights

## Design Principles

1. **Readability**: High contrast text on dark backgrounds
2. **Consistency**: Unified color scheme throughout
3. **Professionalism**: Clean layouts with generous spacing
4. **Accessibility**: Large fonts and clear labels
5. **Elegance**: Subtle gradients and smooth transitions

## Responsive Features

The HTML dashboard adapts to different screen sizes:
- Desktop: Multi-column layouts
- Tablet: Flexible grids
- Mobile: Single column stacking

## Performance

- High-resolution exports (300 DPI) for publications
- Optimized PNG compression
- Lightweight HTML with inline CSS
- No external dependencies for dashboard viewing

## Future Enhancements

Potential additions:
- Interactive Plotly visualizations
- Real-time WebSocket updates
- Experiment filtering and search
- Export to PDF reports
- Dark/light theme toggle
- Customizable color schemes
