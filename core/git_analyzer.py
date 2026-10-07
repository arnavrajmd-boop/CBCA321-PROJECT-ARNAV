from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd
from git import Repo, InvalidGitRepositoryError, NoSuchPathError, GitCommandError


@dataclass
class AnalysisResult:
    developer_summary: pd.DataFrame
    activity: pd.DataFrame
    commits: pd.DataFrame


def validate_repository(repo_path: str) -> bool:
    """
    Checks if the provided path is a valid and readable Git repository.
    Returns False for empty strings, non-directories, or invalid git directories.
    """
    if not repo_path or not str(repo_path).strip():
        return False
    path = Path(repo_path).expanduser()
    if not path.exists() or not path.is_dir():
        return False
    try:
        Repo(path)
        return True
    except (InvalidGitRepositoryError, NoSuchPathError):
        return False
    except Exception:
        return False


def analyze_repository(repo_path: str, max_commits: int = 5000) -> AnalysisResult:
    """
    Analyzes commit history for a local Git repository.
    Extracts author metrics, activity over time, and commit details.
    Handles empty repositories or branch heads without crashing.
    """
    if not repo_path or not str(repo_path).strip():
        raise ValueError("Please provide a valid repository path.")

    path = Path(repo_path).expanduser()
    if not path.exists() or not path.is_dir():
        raise ValueError(f"The path '{repo_path}' does not exist or is not a directory.")

    try:
        repo = Repo(path)
    except (InvalidGitRepositoryError, NoSuchPathError) as exc:
        raise ValueError("The supplied path is not a readable Git repository.") from exc

    # Return empty result safely if repository has no commits yet
    empty_result = AnalysisResult(
        developer_summary=pd.DataFrame(columns=["author", "commits", "files_changed", "additions", "deletions"]),
        activity=pd.DataFrame(columns=["date", "commits", "additions", "deletions"]),
        commits=pd.DataFrame(columns=["commit", "author", "date", "message", "files_changed", "additions", "deletions"]),
    )

    try:
        if not repo.head.is_valid() or not repo.heads:
            return empty_result
    except Exception:
        # Repositories with no HEAD reference
        return empty_result

    rows = []
    try:
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
    except (ValueError, GitCommandError):
        return empty_result

    columns = ["commit", "author", "date", "message", "files_changed", "additions", "deletions"]
    commits = pd.DataFrame(rows, columns=columns)

    if commits.empty:
        return empty_result

    commits["date"] = pd.to_datetime(commits["date"])

    summary = commits.groupby("author", as_index=False).agg(
        commits=("commit", "count"),
        files_changed=("files_changed", "sum"),
        additions=("additions", "sum"),
        deletions=("deletions", "sum"),
    ).sort_values(["commits", "additions"], ascending=False)

    activity = commits.groupby("date", as_index=False).agg(
        commits=("commit", "count"),
        additions=("additions", "sum"),
        deletions=("deletions", "sum"),
    ).sort_values("date")

    return AnalysisResult(developer_summary=summary, activity=activity, commits=commits)


def filter_by_developer(result: AnalysisResult, developer: str) -> AnalysisResult:
    """
    Filters analysis results for a specific developer.
    When developer is 'All developers' or empty, returns the original result.
    """
    if not developer or developer == "All developers":
        return result

    clean_developer = developer.strip()
    commits = result.commits[result.commits["author"] == clean_developer].copy()
    if commits.empty:
        return AnalysisResult(
            developer_summary=pd.DataFrame(columns=["author", "commits", "files_changed", "additions", "deletions"]),
            activity=pd.DataFrame(columns=["date", "commits", "additions", "deletions"]),
            commits=commits,
        )

    summary = commits.groupby("author", as_index=False).agg(
        commits=("commit", "count"),
        files_changed=("files_changed", "sum"),
        additions=("additions", "sum"),
        deletions=("deletions", "sum"),
    ).sort_values(["commits", "additions"], ascending=False)

    activity = commits.groupby("date", as_index=False).agg(
        commits=("commit", "count"),
        additions=("additions", "sum"),
        deletions=("deletions", "sum"),
    ).sort_values("date")

    return AnalysisResult(developer_summary=summary, activity=activity, commits=commits)


def get_developer_list(result: AnalysisResult) -> list[str]:
    """
    Returns a sorted list of unique contributor names in the repository.
    """
    if result.commits.empty or "author" not in result.commits.columns:
        return []
    return sorted(result.commits["author"].dropna().unique().tolist())


def get_developer_stats(result: AnalysisResult, developer: Optional[str] = None) -> dict:
    """
    Calculates detailed contribution metrics for a specific developer or all developers.
    Returns total commits, additions, deletions, changed files, net lines, and active days.
    """
    if developer and developer != "All developers":
        df_commits = result.commits[result.commits["author"] == developer.strip()]
        author_name = developer.strip()
    else:
        df_commits = result.commits
        author_name = "All developers"

    if df_commits.empty:
        return {
            "author": author_name,
            "commits": 0,
            "additions": 0,
            "deletions": 0,
            "files_changed": 0,
            "net_lines": 0,
            "active_days": 0,
            "first_commit_date": "N/A",
            "last_commit_date": "N/A",
        }

    additions = int(df_commits["additions"].sum())
    deletions = int(df_commits["deletions"].sum())

    min_date = df_commits["date"].min()
    max_date = df_commits["date"].max()

    first_date_str = str(min_date.date()) if hasattr(min_date, "date") else str(min_date)
    last_date_str = str(max_date.date()) if hasattr(max_date, "date") else str(max_date)

    return {
        "author": author_name,
        "commits": int(len(df_commits)),
        "additions": additions,
        "deletions": deletions,
        "files_changed": int(df_commits["files_changed"].sum()),
        "net_lines": additions - deletions,
        "active_days": int(df_commits["date"].nunique()),
        "first_commit_date": first_date_str,
        "last_commit_date": last_date_str,
    }
