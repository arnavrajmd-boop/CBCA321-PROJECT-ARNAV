from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from git import Repo, InvalidGitRepositoryError, NoSuchPathError


@dataclass
class AnalysisResult:
    developer_summary: pd.DataFrame
    activity: pd.DataFrame
    commits: pd.DataFrame


def validate_repository(repo_path: str) -> bool:
    path = Path(repo_path).expanduser()
    if not path.exists() or not path.is_dir():
        return False
    try:
        Repo(path)
        return True
    except (InvalidGitRepositoryError, NoSuchPathError):
        return False


def analyze_repository(repo_path: str, max_commits: int = 5000) -> AnalysisResult:
    try:
        repo = Repo(Path(repo_path).expanduser())
    except (InvalidGitRepositoryError, NoSuchPathError) as exc:
        raise ValueError("The supplied path is not a readable Git repository.") from exc

    rows = []
    for commit in repo.iter_commits(max_count=max_commits):
        total = commit.stats.total
        rows.append({
            "commit": commit.hexsha[:8],
            "author": commit.author.name or "Unknown",
            "date": commit.committed_datetime.date(),
            "message": commit.message.strip().splitlines()[0] if commit.message else "",
            "files_changed": len(commit.stats.files),
            "additions": int(total.get("insertions", 0)),
            "deletions": int(total.get("deletions", 0)),
        })

    columns = ["commit","author","date","message","files_changed","additions","deletions"]
    commits = pd.DataFrame(rows, columns=columns)

    if commits.empty:
        return AnalysisResult(
            pd.DataFrame(columns=["author","commits","files_changed","additions","deletions"]),
            pd.DataFrame(columns=["date","commits","additions","deletions"]),
            commits,
        )

    commits["date"] = pd.to_datetime(commits["date"])

    summary = commits.groupby("author", as_index=False).agg(
        commits=("commit", "count"),
        files_changed=("files_changed", "sum"),
        additions=("additions", "sum"),
        deletions=("deletions", "sum"),
    ).sort_values(["commits","additions"], ascending=False)

    activity = commits.groupby("date", as_index=False).agg(
        commits=("commit", "count"),
        additions=("additions", "sum"),
        deletions=("deletions", "sum"),
    ).sort_values("date")

    return AnalysisResult(summary, activity, commits)


def filter_by_developer(result: AnalysisResult, developer: str):
    if not developer or developer == "All developers":
        return result
    commits = result.commits[result.commits["author"] == developer].copy()
    if commits.empty:
        return AnalysisResult(
            pd.DataFrame(columns=["author","commits","files_changed","additions","deletions"]),
            pd.DataFrame(columns=["date","commits","additions","deletions"]),
            commits,
        )

    summary = commits.groupby("author", as_index=False).agg(
        commits=("commit","count"),
        files_changed=("files_changed","sum"),
        additions=("additions","sum"),
        deletions=("deletions","sum"),
    )
    activity = commits.groupby("date", as_index=False).agg(
        commits=("commit","count"),
        additions=("additions","sum"),
        deletions=("deletions","sum"),
    ).sort_values("date")
    return AnalysisResult(summary, activity, commits)
