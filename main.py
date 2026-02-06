"""
Gold & Silver Market Analysis
Main Entry Point

This script serves as a reference entry point for the project.
It documents the analysis workflow and allows selective execution
of data preparation and analysis steps.

Dashboard is launched separately using Streamlit.
"""

from pathlib import Path

# --------------------------------------------------
# PROJECT STRUCTURE OVERVIEW
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
SRC_DIR = BASE_DIR / "src"
DASHBOARD_DIR = BASE_DIR / "dashboard"

print("📊 Gold & Silver Market Analysis Project")
print("-" * 45)

print("Project structure:")
print(f"- Data directory:      {DATA_DIR}")
print(f"- Analysis scripts:    {SRC_DIR / 'analysis'}")
print(f"- Dashboard app:       {DASHBOARD_DIR / 'app.py'}")

print("\nWorkflow:")
print("1. Raw data is cleaned and processed (src/data)")
print("2. Market analysis and backtesting are performed (src/analysis)")
print("3. Insights are presented via Streamlit dashboard (dashboard/app.py)")

print("\nTo run the dashboard:")
print("python -m streamlit run dashboard/app.py")

print("\nNote:")
print("This project focuses on analytical validation and insight communication,")
print("not automated trading or prediction.")

print("\n✅ Project setup complete.")
