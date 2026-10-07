# Developer Contribution Visualizer

**CBCA321 Project #6**  
**Student:** Arnav Rajput  
**Enrollment:** S24BCAU0194  

---

## Overview

The **Developer Contribution Visualizer** is a Python and Streamlit desktop web application that analyzes local Git repositories. It turns raw commit histories into structured developer contribution metrics, interactive visual charts, and filterable tables.

---

## Assessment 3: Feature Implementation

### 1. Crucial Feature Implemented
**End-to-End Developer Contribution Analysis & Reactive Developer Filtering**

In Assessment 3, the developer contribution analysis and filtering capability was developed into a near-complete, production-grade feature connecting the presentation layer, analytical business logic, and automated tests.

---

### 2. How the Feature Works

1. **Repository Ingestion & Validation**:
   - The user inputs any local Git directory path into the sidebar.
   - The backend validates that the path exists, is a directory, and contains a readable Git repository before attempting to parse commit objects.
   - Empty repositories (zero commits) and invalid paths are caught gracefully with friendly alerts instead of application crashes.

2. **Contribution Aggregation**:
   - Commit history is processed using `GitPython` to extract author identities, commit hashes, dates, messages, file count, insertions (additions), and deletions.
   - Metrics are aggregated by author and by date using `pandas`.

3. **Reactive Contributor Filtering**:
   - The sidebar dynamically populates a dropdown with all unique contributors found in the repository, along with an **"All developers"** option.
   - Selecting an individual contributor immediately updates all components across the dashboard:
     - **Profile Banner**: Displays the contributor's name, commit count, percentage share of total repository commits, active days, and active date span.
     - **KPI Metric Cards**: Displays individual commits, total additions, total deletions, and files changed with contextual indicators (net lines added, active days).
     - **Code Impact Chart**: Displays a dedicated comparison bar chart of Lines Added vs. Lines Deleted for that contributor.
     - **Activity Over Time Chart**: Plots the contributor's specific timeline of commits, additions, and deletions over time.
     - **Contribution Summary Table**: Isolates the contributor's aggregated metrics.
     - **Commit Details Table**: Lists only commits authored by that specific contributor, sorted in reverse-chronological order.

4. **All-Developers View**:
   - Selecting "All developers" preserves the global view, showing team-wide commit rankings, overall repo velocity, and full commit histories.

---

### 3. Changes in Business Logic (`core/git_analyzer.py`)

- **Edge-Case Validation (`validate_repository`)**:
  - Validates against empty strings, whitespace, and non-directories before invoking GitPython constructors.
- **Empty & Headless Repository Safety (`analyze_repository`)**:
  - Safely checks `repo.head.is_valid()` and handles `GitCommandError` and `ValueError` for newly initialized repositories with zero commits, returning structured empty DataFrames rather than crashing.
- **Author Discovery (`get_developer_list`)**:
  - Added helper to extract a clean, sorted list of unique contributor names.
- **Detailed Contributor Statistics (`get_developer_stats`)**:
  - Added helper calculating total commits, additions, deletions, changed files, net code volume (`additions - deletions`), count of unique active days, first commit date, and last commit date.
- **Robust Filtering (`filter_by_developer`)**:
  - Handles string whitespace trimming, cleanly falls back to the full dataset when "All developers" is selected, and produces a valid empty schema when filtering for non-existent authors.

---

### 4. Changes in User Interface (`app/main.py`)

- **Error Resilience & State Reset**:
  - Added explicit session state cleanup and a **Reset** button to prevent previous analysis data from persisting when an invalid path or new repository is analyzed.
- **Viva-Ready Contributor Filter**:
  - Integrated the contributor dropdown in the sidebar with live repository metadata (total contributors count, total commit count).
- **Contributor Profile Header**:
  - Highlights the selected contributor's role with a percentage calculation (`X% of total repo commits`) and active timeframe.
- **Adaptive Visualizations**:
  - **Left Chart**: Dynamically renders "Commits by Developer" in team view, and shifts to "Code Impact: Lines Added vs Deleted" with distinct color styling (`#10b981` green for additions, `#ef4444` red for deletions) in contributor view.
  - **Right Chart**: Plots date-based project velocity, responding directly to the developer filter.
- **Formatted Tables**:
  - Standardized column headers and formatted dates to ISO `YYYY-MM-DD` strings for readability during demonstrations.

---

## Project Structure

```text
Developer_Contribution_Visualizer/
├── app/
│   └── main.py                   # Streamlit UI: layout, filtering controls, charts, and tables
├── core/
│   ├── __init__.py               # Core package initializer
│   └── git_analyzer.py           # Business logic: extraction, aggregation, filtering, stats helpers
├── output/
│   └── Project assessment-2 Deliverable-1.pdf # Assessment documentation and report
├── tests/
│   └── test_git_analyzer.py      # Automated pytest test suite
├── .gitignore                    # Python, virtualenv, and IDE ignore rules
├── Assessment-2.md               # Deliverable specifications
├── README.md                     # Complete project and feature documentation
└── requirements.txt              # Project dependencies
```

---

## How to Run the Application

### 1. Prerequisites
- **Python**: Version 3.10 or higher (Python 3.11 recommended)
- **Git**: Installed and accessible in your system terminal

### 2. Activate the Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

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
pip install -r requirements.txt
```

### 4. Start the Dashboard
```powershell
streamlit run app/main.py
```

Open your browser at `http://localhost:8501`. Enter any local Git repository path (e.g. `D:\CLOUD PRO\CBCA321-PROJECT-ARNAV`) and click **Analyze**.

---

## How to Run the Automated Tests

Automated tests run against dynamically generated Git repositories created in temporary folders (`tmp_path`), testing multi-author history without modifying any user repositories.

Run the test suite with verbose output:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

### Test Suite Results:

```text
tests/test_git_analyzer.py::test_validate_repository PASSED              [ 12%]
tests/test_git_analyzer.py::test_validate_repository_edge_cases PASSED   [ 25%]
tests/test_git_analyzer.py::test_analysis PASSED                         [ 37%]
tests/test_git_analyzer.py::test_analysis_empty_repo PASSED              [ 50%]
tests/test_git_analyzer.py::test_analysis_invalid_path PASSED            [ 62%]
tests/test_git_analyzer.py::test_filter PASSED                           [ 75%]
tests/test_git_analyzer.py::test_multi_author_analysis_and_filtering PASSED [ 87%]
tests/test_git_analyzer.py::test_get_developer_stats PASSED              [100%]

============================== 8 passed in 6.27s ==============================
```

### What Each Test Verifies:
1. `test_validate_repository`: Verifies valid vs invalid repository paths.
2. `test_validate_repository_edge_cases`: Verifies blank strings, whitespace, and non-directory files return `False`.
3. `test_analysis`: Verifies commit extraction and metric aggregation.
4. `test_analysis_empty_repo`: Verifies that initialized Git repos with zero commits return empty DataFrames safely.
5. `test_analysis_invalid_path`: Verifies informative `ValueError` exceptions for missing directories.
6. `test_filter`: Verifies developer filtering on a single-author repo.
7. `test_multi_author_analysis_and_filtering`: Verifies multi-author extraction (`Alice` and `Bob`), individual author filtering, `All developers` fallback, and non-existent author safety.
8. `test_get_developer_stats`: Verifies calculation of commits, additions, deletions, changed files, active days, and date ranges.

---

## Architecture

```text
┌────────────────────────────────────────────────────────┐
│                   Streamlit Dashboard                  │ (app/main.py)
│  • Sidebar: Path input, Validation, Contributor Filter │
│  • Contributor Profile & Share Banner                  │
│  • 4 KPI Cards: Commits, Additions, Deletions, Files   │
│  • Dynamic Charts: Impact & Timeline Velocity          │
│  • Filtered Data Tables: Summary & Commit Details      │
└───────────────────────────┬────────────────────────────┘
                            │
               calls analyze_repository()
               calls filter_by_developer()
               calls get_developer_stats()
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Git Analyzer Logic                   │ (core/git_analyzer.py)
│  • Repository Path Validation                          │
│  • Git Commit & Diff Stats Extraction                  │
│  • Multi-author Aggregation & Filtering Logic          │
│  • Metric Computation (Net lines, Active days, Dates)  │
└───────────────────────────┬────────────────────────────┘
                            │
                   reads via GitPython
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                  Local Git Repository                  │ (.git metadata)
└────────────────────────────────────────────────────────┘
```

---

## Key Learnings

1. **Defensive API Contracts**: Git repositories in the wild have edge cases such as newly initialized empty repositories, bare repositories, and headless branches. Defensive error handling in the data extraction layer is essential to keep web interfaces responsive and stable.
2. **Deterministic Multi-Author Fixtures**: Using `git.Actor` in pytest fixtures enables repeatable multi-developer testing of complex filtering and metric computations without external network dependencies.
3. **Cohesive UI Reactivity**: A filtering feature is only complete when all analytical components—KPIs, comparison charts, time series, and raw logs—consistently reflect the selected filter criteria.
4. **Separation of Presentation and Business Logic**: Keeping computation in `core/` and visualization in `app/` allows 100% of the analytical routines to be tested automatically through standard CI/CD frameworks.
