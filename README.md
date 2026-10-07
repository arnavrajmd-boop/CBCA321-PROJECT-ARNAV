# Developer Contribution Visualizer

**CBCA321 Project #6**  
**Student:** Arnav Rajput  
**Enrollment:** S24BCAU0194  

---

## Overview

The **Developer Contribution Visualizer** is a desktop web application built with Python and Streamlit that analyzes local Git repositories. It parses commit history, extracts contribution metadata, and presents developer activity through interactive charts, metric summaries, and detailed tables.

---

## Project Structure

```text
Developer_Contribution_Visualizer/
├── app/
│   └── main.py                   # Streamlit dashboard UI and visualization layout
├── core/
│   ├── __init__.py               # Core package initializer
│   └── git_analyzer.py           # Git history extraction, validation, and data aggregation logic
├── output/
│   └── Project assessment-2 Deliverable-1.pdf # Deliverable documentation and report
├── tests/
│   └── test_git_analyzer.py      # Automated unit tests for Git analyzer functions
├── .gitignore                    # Git ignore file for Python, virtual environments, and caches
├── Assessment-2.md               # Assessment specifications, rubric alignment, and scope details
├── README.md                     # Project documentation and setup guide
└── requirements.txt              # Production and testing dependencies
```

### Component Roles

- **`app/main.py`**: Presentation layer built using Streamlit and Plotly. Handles user input, sidebar controls, metric cards, charts, and table presentation.
- **`core/git_analyzer.py`**: Business logic layer. Uses `GitPython` to read repository commits and `pandas` to structure and aggregate author metrics and timeline trends. Separated from the UI for independent testability.
- **`tests/test_git_analyzer.py`**: Test suite using `pytest`. Uses temporary in-memory/on-disk repositories created via `tmp_path` to test validation, metric aggregation, and developer filtering.
- **`requirements.txt`**: Pins dependencies to stable, compatible versions (`streamlit`, `gitpython`, `pandas`, `plotly`, `pytest`).

---

## Dashboard Metrics & Features

When analyzing a repository, the dashboard calculates and displays:

### 1. Summary Metric Cards
- **Commits**: Total number of commits analyzed (overall or for the selected developer).
- **Lines Added**: Total number of lines inserted across commits (`insertions`).
- **Lines Deleted**: Total number of lines removed across commits (`deletions`).
- **Files Changed**: Cumulative count of files modified across commits.

### 2. Interactive Charts
- **Commits by Developer (Bar Chart)**: Compares total commit contributions across all contributors.
- **Activity Over Time (Line Chart)**: Tracks historical project velocity over dates, plotting commits, additions, and deletions simultaneously with interactive hover tooltips.

### 3. Data Tables
- **Contribution Summary Table**: Aggregated developer metrics displaying author name, total commits, files changed, total additions, and total deletions.
- **Commit Details Table**: Reverse-chronological table of commits displaying commit hash (short 8-character SHA), author name, date, commit message headline, files changed, additions, and deletions.

### 4. Interactive Filtering & Validation
- **Path Input**: Enter any local Git repository path to analyze.
- **Repository Validation**: Validates that the provided path exists, is a directory, and contains a valid Git repository; displays clear error messages for invalid paths.
- **Developer Filter**: Sidebar dropdown allowing users to view metrics for "All developers" or filter all KPIs, charts, and tables for an individual developer.

---

## Prerequisites

- **Python**: Version 3.10 or higher
- **Git**: Installed and available in your system `PATH`

---

## Setup Instructions

### 1. Create a Virtual Environment

Open PowerShell (Windows) or Terminal (Linux/macOS) in the project directory:

```bash
python -m venv .venv
```

### 2. Activate the Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` first)*

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## How to Run the Application

Once dependencies are installed and the virtual environment is active:

```bash
streamlit run app/main.py
```

1. Streamlit will launch the local web server and open your browser automatically at:
   ```text
   http://localhost:8501
   ```
2. In the sidebar on the left:
   - Enter the full path of any local Git repository (for example: `D:\CLOUD PRO\CBCA321-PROJECT-ARNAV` or your current repo path).
   - Click **Analyze Repository**.
3. Use the **Developer filter** in the sidebar to switch between overall repository activity and developer-specific stats.

---

## How to Run the Tests

Automated unit tests verify the analysis logic independently from the UI without modifying any real repositories.

To run the test suite:

```bash
pytest -q
```

Or for verbose output with individual test names:

```bash
pytest -v
```

### Test Coverage Summary:
- **`test_validate_repository`**: Verifies that valid Git repositories are recognized and non-existent/invalid directories return `False`.
- **`test_analysis`**: Verifies accurate commit counting and developer aggregation from repository commit logs.
- **`test_filter`**: Verifies that developer filtering isolates the selected contributor's records correctly.

---

## Architecture

```text
┌───────────────────────────────┐
│     Streamlit Dashboard       │  (app/main.py)
│    • Sidebar inputs & filter  │
│    • KPI metric cards         │
│    • Plotly charts & tables   │
└───────────────┬───────────────┘
                │ calls analyze_repository() / filter_by_developer()
                ▼
┌───────────────────────────────┐
│      Git Analyzer Logic       │  (core/git_analyzer.py)
│    • Repo validation          │
│    • Commit iteration         │
│    • Pandas aggregation       │
└───────────────┬───────────────┘
                │ reads via GitPython
                ▼
┌───────────────────────────────┐
│     Local Git Repository      │  (.git metadata & commit objects)
└───────────────────────────────┘
```

---

## Key Learnings

1. **Structured Git Extraction**: Git commits and diff stats can be converted directly into structured tabular data using `GitPython` and `pandas`.
2. **Layered Architecture**: Decoupling data extraction and aggregation logic from the Streamlit UI makes the core analytical routines testable with automated pytest fixtures.
3. **Descriptive Analytics**: Aggregating raw commit data into developer summaries and time series helps visualize team activity and code churn effectively.
