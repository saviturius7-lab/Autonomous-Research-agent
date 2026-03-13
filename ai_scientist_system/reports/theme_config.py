"""Centralized theme configuration for consistent styling across visualizations."""

from __future__ import annotations

from typing import Dict


class VisualTheme:
    """Evening pink color theme for AI Scientist visualizations."""

    EVENING_PINK = {
        "background": "#2a1a2e",
        "surface": "#3d2c45",
        "primary": "#e84393",
        "secondary": "#fd79a8",
        "tertiary": "#fab1a0",
        "accent": "#ffeaa7",
        "text_primary": "#ffffff",
        "text_secondary": "#dfe6e9",
        "grid": "#574b60",
        "gradient_start": "#e84393",
        "gradient_end": "#fd79a8",
        "success": "#55efc4",
        "success_bg": "rgba(0, 184, 148, 0.3)",
        "warning": "#ffeaa7",
        "warning_bg": "rgba(255, 234, 167, 0.3)",
        "error": "#ff7675",
        "error_bg": "rgba(255, 118, 117, 0.3)",
    }

    @classmethod
    def get_theme(cls, theme_name: str = "evening_pink") -> Dict[str, str]:
        if theme_name == "evening_pink":
            return cls.EVENING_PINK
        return cls.EVENING_PINK

    @classmethod
    def get_color(cls, color_name: str, theme_name: str = "evening_pink") -> str:
        theme = cls.get_theme(theme_name)
        return theme.get(color_name, "#ffffff")

    @classmethod
    def get_matplotlib_params(cls, theme_name: str = "evening_pink") -> Dict[str, str]:
        theme = cls.get_theme(theme_name)
        return {
            "figure.facecolor": theme["background"],
            "axes.facecolor": theme["surface"],
            "axes.edgecolor": theme["grid"],
            "axes.labelcolor": theme["text_primary"],
            "axes.titlecolor": theme["text_primary"],
            "text.color": theme["text_primary"],
            "xtick.color": theme["text_secondary"],
            "ytick.color": theme["text_secondary"],
            "grid.color": theme["grid"],
            "grid.alpha": 0.3,
            "font.family": "sans-serif",
            "font.size": 10,
        }

    @classmethod
    def get_css_variables(cls, theme_name: str = "evening_pink") -> str:
        theme = cls.get_theme(theme_name)
        css_vars = []
        for key, value in theme.items():
            css_var = f"--{key.replace('_', '-')}: {value};"
            css_vars.append(css_var)
        return "\n    ".join(css_vars)
