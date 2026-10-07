# Developer Contribution Visualizer

CBCA321 Project #6  
**Student:** Arnav Rajput  
**Enrollment:** S24BCAU0194

## What this project does

This application analyzes a local Git repository and turns its history into contribution statistics and interactive charts.

## First Deliverable

- Repository validation
- Commit extraction
- Developer-wise commits
- Additions and deletions
- Changed files
- Activity over time
- Developer filtering
- Interactive dashboard
- Unit tests

## Setup

Requires Python 3.10+ and Git.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/WSL:
```bash
source .venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Run tests:
```bash
pytest -q
```

Run dashboard:
```bash
streamlit run app/main.py
```

Enter the path of a local Git repository and click **Analyze Repository**.

## Architecture

```text
Streamlit UI
     |
     v
Git Analyzer
     |
     v
Local Git Repository
```

## Learnings

1. Git history can be treated as structured contribution data.
2. Separating analysis from presentation makes testing easier.
3. Aggregating commits by developer makes raw history easier to understand.
4. Charts make contribution patterns easier to compare.
