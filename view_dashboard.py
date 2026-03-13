"""Quick script to open the latest dashboard in browser."""

import webbrowser
from pathlib import Path


def find_latest_dashboard():
    reports_dir = Path("artifacts/reports")
    if not reports_dir.exists():
        print("No reports directory found. Run the system first with: python3 main.py")
        return None

    dashboards = sorted(reports_dir.glob("dashboard_*.html"))
    if not dashboards:
        print("No dashboards found. Run the system first with: python3 main.py")
        return None

    return dashboards[-1]


def main():
    dashboard = find_latest_dashboard()
    if dashboard:
        print(f"Opening: {dashboard}")
        webbrowser.open(f"file://{dashboard.absolute()}")
        print("Dashboard opened in your default browser!")
    else:
        print("\nTo generate dashboards:")
        print("1. python3 generate_sample_data.py")
        print("2. python3 main.py")


if __name__ == "__main__":
    main()
