"""Preview the evening pink theme visualizations."""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

EVENING_PINK_THEME = {
    "background": "#2a1a2e",
    "surface": "#3d2c45",
    "primary": "#e84393",
    "secondary": "#fd79a8",
    "tertiary": "#fab1a0",
    "accent": "#ffeaa7",
    "text_primary": "#ffffff",
    "text_secondary": "#dfe6e9",
    "grid": "#574b60",
}


def configure_evening_pink_style():
    plt.rcParams.update({
        "figure.facecolor": EVENING_PINK_THEME["background"],
        "axes.facecolor": EVENING_PINK_THEME["surface"],
        "axes.edgecolor": EVENING_PINK_THEME["grid"],
        "axes.labelcolor": EVENING_PINK_THEME["text_primary"],
        "axes.titlecolor": EVENING_PINK_THEME["text_primary"],
        "text.color": EVENING_PINK_THEME["text_primary"],
        "xtick.color": EVENING_PINK_THEME["text_secondary"],
        "ytick.color": EVENING_PINK_THEME["text_secondary"],
        "grid.color": EVENING_PINK_THEME["grid"],
        "grid.alpha": 0.3,
        "font.family": "sans-serif",
        "font.size": 10,
    })


def create_sample_leaderboard():
    configure_evening_pink_style()

    experiments = [f"exp_{i:06d}" for i in range(1, 11)]
    scores = np.array([0.892, 0.885, 0.878, 0.871, 0.865, 0.859, 0.852, 0.846, 0.839, 0.832])

    fig, ax = plt.subplots(figsize=(14, 7))

    x_positions = np.arange(len(experiments))
    colors = plt.cm.RdPu_r(np.linspace(0.3, 0.8, len(experiments)))

    bars = ax.bar(
        x_positions,
        scores,
        color=colors,
        edgecolor=EVENING_PINK_THEME["primary"],
        linewidth=1.5,
        alpha=0.9,
    )

    for bar, value in zip(bars, scores):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.01,
            f"{value:.3f}",
            ha="center",
            va="bottom",
            color=EVENING_PINK_THEME["accent"],
            fontsize=9,
            fontweight="bold",
        )

    ax.set_xlabel("Experiment ID", fontsize=12, fontweight="bold")
    ax.set_ylabel("F1 SCORE", fontsize=12, fontweight="bold")
    ax.set_title(
        "Top 10 Experiments by F1 Score",
        fontsize=16,
        fontweight="bold",
        color=EVENING_PINK_THEME["primary"],
        pad=20,
    )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(experiments, rotation=45, ha="right", fontsize=9)
    ax.grid(True, axis="y", alpha=0.3, linestyle="--", linewidth=0.7)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    output_dir = Path("artifacts/preview")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        output_dir / "sample_leaderboard.png",
        dpi=300,
        bbox_inches="tight",
        facecolor=EVENING_PINK_THEME["background"],
    )
    print(f"Saved: {output_dir / 'sample_leaderboard.png'}")
    plt.close()


def create_sample_metrics():
    configure_evening_pink_style()

    experiments = [f"exp_{i:06d}" for i in range(1, 6)]
    metrics_names = ["accuracy", "precision", "recall", "f1"]

    fig, ax = plt.subplots(figsize=(12, 8))

    x_positions = np.arange(len(experiments))
    bar_width = 0.2

    colors = [
        EVENING_PINK_THEME["primary"],
        EVENING_PINK_THEME["secondary"],
        EVENING_PINK_THEME["tertiary"],
        EVENING_PINK_THEME["accent"],
    ]

    np.random.seed(42)
    for i, metric_name in enumerate(metrics_names):
        values = 0.75 + np.random.rand(len(experiments)) * 0.15
        offset = (i - len(metrics_names) / 2) * bar_width + bar_width / 2
        ax.bar(
            x_positions + offset,
            values,
            bar_width,
            label=metric_name.upper(),
            color=colors[i],
            alpha=0.85,
            edgecolor=EVENING_PINK_THEME["background"],
            linewidth=1.2,
        )

    ax.set_xlabel("Experiment ID", fontsize=12, fontweight="bold")
    ax.set_ylabel("Score", fontsize=12, fontweight="bold")
    ax.set_title(
        "Metrics Comparison - Top 5 Experiments",
        fontsize=16,
        fontweight="bold",
        color=EVENING_PINK_THEME["primary"],
        pad=20,
    )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(experiments, rotation=45, ha="right", fontsize=9)
    ax.legend(
        loc="upper right",
        framealpha=0.9,
        facecolor=EVENING_PINK_THEME["surface"],
        edgecolor=EVENING_PINK_THEME["grid"],
    )
    ax.grid(True, axis="y", alpha=0.3, linestyle="--", linewidth=0.7)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    output_dir = Path("artifacts/preview")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        output_dir / "sample_metrics.png",
        dpi=300,
        bbox_inches="tight",
        facecolor=EVENING_PINK_THEME["background"],
    )
    print(f"Saved: {output_dir / 'sample_metrics.png'}")
    plt.close()


def create_sample_features():
    configure_evening_pink_style()

    features = [f"feature_{i}" for i in range(15)]
    importances = np.sort(np.random.rand(15) * 0.3 + 0.05)[::-1]

    fig, ax = plt.subplots(figsize=(10, 8))

    y_positions = np.arange(len(features))
    colors = plt.cm.RdPu_r(np.linspace(0.3, 0.8, len(features)))

    bars = ax.barh(
        y_positions,
        importances,
        color=colors,
        edgecolor=EVENING_PINK_THEME["primary"],
        linewidth=1.5,
        alpha=0.9,
    )

    for bar, value in zip(bars, importances):
        width = bar.get_width()
        ax.text(
            width + 0.005,
            bar.get_y() + bar.get_height() / 2.0,
            f"{value:.4f}",
            ha="left",
            va="center",
            color=EVENING_PINK_THEME["accent"],
            fontsize=8,
            fontweight="bold",
        )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(features, fontsize=9)
    ax.set_xlabel("Importance", fontsize=12, fontweight="bold")
    ax.set_title(
        "Top 15 Feature Importances",
        fontsize=16,
        fontweight="bold",
        color=EVENING_PINK_THEME["primary"],
        pad=20,
    )

    ax.grid(True, axis="x", alpha=0.3, linestyle="--", linewidth=0.7)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    output_dir = Path("artifacts/preview")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        output_dir / "sample_features.png",
        dpi=300,
        bbox_inches="tight",
        facecolor=EVENING_PINK_THEME["background"],
    )
    print(f"Saved: {output_dir / 'sample_features.png'}")
    plt.close()


if __name__ == "__main__":
    print("Generating evening pink theme visualization previews...")
    create_sample_leaderboard()
    create_sample_metrics()
    create_sample_features()
    print("\nAll previews generated successfully!")
    print("Check artifacts/preview/ directory")
