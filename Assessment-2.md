# CBCA321 Project Assessment 2 — Deliverable 1

**Student:** Arnav Rajput  
**Enrollment:** S24BCAU0194  
**Project:** #6 — Developer Contribution Visualizer

## 1. Finalized Project Title
**Developer Contribution Visualizer**

A dashboard that reads a Git repository and presents developer contribution information such as commits, changed files, additions, deletions, and activity over time.

## 2. Major Components

### UI
- Streamlit dashboard
- Repository path input
- Developer filter
- Summary cards
- Charts and commit table

### Persistence / Data
- Git repository history is the primary data source.
- Pandas DataFrames hold analyzed data for Deliverable 1.
- SQLite can be added later if persistent snapshots are required.

### Logic
- Repository validation
- Git history extraction
- Contribution aggregation
- Time-based activity calculation
- Filtering

## 3. Architecture

```text
Streamlit UI
     |
     v
Analysis / Business Logic
     |
     v
Local Git Repository
```

The UI is separated from the analysis logic so that the core functions can be unit-tested independently.

## 4. Minimal Features for Deliverable 1

1. Accept a local Git repository path.
2. Validate the repository.
3. Read commit history.
4. Identify authors.
5. Count commits by developer.
6. Calculate additions and deletions.
7. Count changed files.
8. Show activity over time.
9. Filter by developer.
10. Display an interactive dashboard.
11. Handle invalid repositories clearly.
12. Provide unit tests.

## 5. Users

- **Developers:** inspect contribution history.
- **Team Leads:** understand team activity patterns.
- **Project Managers:** view summarized development activity.

The system is descriptive and is not an automatic employee-performance scoring tool.

## 6. Components

| Component | Responsibility |
|---|---|
| `app/main.py` | Streamlit interface |
| `core/git_analyzer.py` | Git extraction and analysis |
| `tests/test_git_analyzer.py` | Unit tests |
| `requirements.txt` | Dependencies |
| `README.md` | Setup and learning notes |

## 7. Interfaces

The UI calls:

```python
analyze_repository(repo_path: str)
```

The analyzer returns structured data for:
- developer summary
- activity over time
- commit details

## 8. Technology Stack

- Python 3.10+
- Streamlit
- GitPython
- Pandas
- Plotly
- Pytest
- Git / GitHub

## 9. Scope

**Included:** local Git analysis, contributor metrics, commits, files changed, additions, deletions, time activity, filtering, charts, tests.

**Excluded:** authentication, private GitHub API integration, cloud deployment, predictive analytics, employee scoring, automatic scheduled analysis.

## 10. Assumptions and Constraints

- Git is installed on the machine.
- The repository is readable.
- Contributor identity comes from Git author information.
- Very large repositories may require optimization.
- Deliverable 1 focuses on local repositories.

## 11. Acceptance Criteria

The deliverable is functional when a valid repository can be loaded, contribution metrics are displayed, activity is visualized, developer filtering works, invalid paths show an error, and the core analysis tests pass.

## 12. Commit Plan

Suggested meaningful commits:
1. Initial project structure and Assessment-2
2. Add Git analyzer
3. Add contribution metrics
4. Add dashboard
5. Add tests and documentation

The course requires commits on at least two different days, so the actual GitHub history should contain genuine commits made on separate days.
