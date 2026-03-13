"""HTML dashboard generator with evening pink theme."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from ai_scientist_system.memory.leaderboard import Leaderboard
from ai_scientist_system.memory.research_memory import ResearchMemory


def generate_dashboard_html(
    iteration: int,
    memory: ResearchMemory,
    leaderboard: Leaderboard,
    patterns: Dict,
    budget_snapshot: Dict,
    report_dir: Path,
) -> Path:
    top_entries = leaderboard.top(10)

    leaderboard_rows = ""
    for i, entry in enumerate(top_entries, 1):
        leaderboard_rows += f"""
        <tr>
            <td>{i}</td>
            <td><span class="experiment-id">{entry.experiment_id}</span></td>
            <td>{entry.model_name}</td>
            <td><span class="metric-value">{entry.metric:.4f}</span></td>
            <td><span class="{'badge-success' if entry.passed_statistics else 'badge-pending'}">
                {'Validated' if entry.passed_statistics else 'Pending'}
            </span></td>
        </tr>
        """

    top_features = patterns.get("top_features", [])[:10]
    feature_list = "".join([f"<li>{feat}</li>" for feat in top_features])

    top_models = patterns.get("top_models", [])[:5]
    model_list = "".join([f"<li>{model}</li>" for model in top_models])

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Scientist Dashboard - Iteration {iteration}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2a1a2e 0%, #3d2c45 100%);
            color: #ffffff;
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 40px;
            background: rgba(61, 44, 69, 0.6);
            border-radius: 15px;
            border: 2px solid #e84393;
            box-shadow: 0 8px 32px rgba(232, 67, 147, 0.2);
        }}

        h1 {{
            font-size: 2.5rem;
            color: #e84393;
            margin-bottom: 10px;
            font-weight: 700;
            letter-spacing: 1px;
        }}

        .subtitle {{
            color: #fd79a8;
            font-size: 1.1rem;
            font-weight: 300;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: rgba(61, 44, 69, 0.8);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #574b60;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(232, 67, 147, 0.3);
            border-color: #e84393;
        }}

        .stat-label {{
            color: #dfe6e9;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}

        .stat-value {{
            color: #fd79a8;
            font-size: 2rem;
            font-weight: 700;
        }}

        .section {{
            background: rgba(61, 44, 69, 0.6);
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 15px;
            border: 1px solid #574b60;
        }}

        .section-title {{
            color: #e84393;
            font-size: 1.8rem;
            margin-bottom: 20px;
            font-weight: 600;
            border-bottom: 2px solid #e84393;
            padding-bottom: 10px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        th {{
            background: rgba(232, 67, 147, 0.2);
            color: #fd79a8;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 1px;
        }}

        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #574b60;
            color: #dfe6e9;
        }}

        tr:hover {{
            background: rgba(232, 67, 147, 0.1);
        }}

        .experiment-id {{
            color: #ffeaa7;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }}

        .metric-value {{
            color: #fd79a8;
            font-weight: 700;
            font-size: 1.1rem;
        }}

        .badge-success {{
            background: rgba(0, 184, 148, 0.3);
            color: #55efc4;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }}

        .badge-pending {{
            background: rgba(253, 121, 168, 0.3);
            color: #fd79a8;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }}

        .visualization-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-top: 20px;
        }}

        .viz-container {{
            background: rgba(61, 44, 69, 0.4);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #574b60;
        }}

        .viz-container img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            display: block;
        }}

        .viz-title {{
            color: #fd79a8;
            font-size: 1.2rem;
            margin-bottom: 15px;
            font-weight: 600;
        }}

        .pattern-list {{
            list-style: none;
            padding: 0;
        }}

        .pattern-list li {{
            padding: 10px 15px;
            margin: 8px 0;
            background: rgba(232, 67, 147, 0.1);
            border-left: 3px solid #e84393;
            border-radius: 4px;
            color: #dfe6e9;
        }}

        .two-column {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}

        @media (max-width: 768px) {{
            .two-column {{
                grid-template-columns: 1fr;
            }}

            .visualization-grid {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 2rem;
            }}
        }}

        .progress-bar {{
            background: rgba(87, 75, 96, 0.5);
            height: 8px;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 10px;
        }}

        .progress-fill {{
            background: linear-gradient(90deg, #e84393, #fd79a8);
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>AI Scientist Research Dashboard</h1>
            <p class="subtitle">Iteration {iteration} | Autonomous Governed Experimentation</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Experiments</div>
                <div class="stat-value">{len(memory.entries)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Experiments Run</div>
                <div class="stat-value">{budget_snapshot.get('experiments_run', 0)}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {(budget_snapshot.get('experiments_run', 0) / budget_snapshot.get('max_experiments', 1)) * 100}%"></div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">API Calls</div>
                <div class="stat-value">{budget_snapshot.get('api_calls', 0)}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {(budget_snapshot.get('api_calls', 0) / budget_snapshot.get('max_api_calls', 1)) * 100}%"></div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Runtime Hours</div>
                <div class="stat-value">{budget_snapshot.get('runtime_hours', 0):.2f}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {(budget_snapshot.get('runtime_hours', 0) / budget_snapshot.get('max_runtime_hours', 1)) * 100}%"></div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">Top Performing Experiments</h2>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Experiment ID</th>
                        <th>Model</th>
                        <th>F1 Score</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {leaderboard_rows}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2 class="section-title">Visualizations</h2>
            <div class="visualization-grid">
                <div class="viz-container">
                    <div class="viz-title">Leaderboard</div>
                    <img src="leaderboard_{iteration:04d}.png" alt="Leaderboard">
                </div>
                <div class="viz-container">
                    <div class="viz-title">Metrics Comparison</div>
                    <img src="metrics_comparison_{iteration:04d}.png" alt="Metrics Comparison">
                </div>
                <div class="viz-container">
                    <div class="viz-title">Feature Importance</div>
                    <img src="feature_importance_{iteration:04d}.png" alt="Feature Importance">
                </div>
            </div>
        </div>

        <div class="two-column">
            <div class="section">
                <h2 class="section-title">Top Features</h2>
                <ul class="pattern-list">
                    {feature_list}
                </ul>
            </div>

            <div class="section">
                <h2 class="section-title">Top Models</h2>
                <ul class="pattern-list">
                    {model_list}
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
    """

    output_path = report_dir / f"dashboard_{iteration:04d}.html"
    output_path.write_text(html_content)
    return output_path
