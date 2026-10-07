import pytest
from git import Repo, Actor
from core.git_analyzer import (
    analyze_repository,
    validate_repository,
    filter_by_developer,
    get_developer_list,
    get_developer_stats,
)


def make_repo(tmp_path):
    path = tmp_path / "demo"
    path.mkdir()
    repo = Repo.init(path)
    f = path / "hello.txt"
    f.write_text("hello\n", encoding="utf-8")
    repo.index.add(["hello.txt"])
    repo.index.commit("first")
    f.write_text("hello\nworld\n", encoding="utf-8")
    repo.index.add(["hello.txt"])
    repo.index.commit("second")
    return path


def make_multi_author_repo(tmp_path):
    path = tmp_path / "multi_repo"
    path.mkdir()
    repo = Repo.init(path)

    alice = Actor("Alice", "alice@example.com")
    bob = Actor("Bob", "bob@example.com")

    # Alice commit 1
    f1 = path / "alice_file.txt"
    f1.write_text("line 1\nline 2\n", encoding="utf-8")
    repo.index.add(["alice_file.txt"])
    repo.index.commit("Alice added file", author=alice, committer=alice)

    # Bob commit 1
    f2 = path / "bob_file.txt"
    f2.write_text("bob content\n", encoding="utf-8")
    repo.index.add(["bob_file.txt"])
    repo.index.commit("Bob added file", author=bob, committer=bob)

    # Alice commit 2
    f1.write_text("line 1\nline 2\nline 3\n", encoding="utf-8")
    repo.index.add(["alice_file.txt"])
    repo.index.commit("Alice updated file", author=alice, committer=alice)

    return path


def test_validate_repository(tmp_path):
    path = make_repo(tmp_path)
    assert validate_repository(str(path))
    assert not validate_repository(str(tmp_path / "bad"))


def test_validate_repository_edge_cases(tmp_path):
    assert not validate_repository("")
    assert not validate_repository("   ")
    regular_file = tmp_path / "regular.txt"
    regular_file.write_text("not a dir", encoding="utf-8")
    assert not validate_repository(str(regular_file))


def test_analysis(tmp_path):
    result = analyze_repository(str(make_repo(tmp_path)))
    assert len(result.commits) == 2
    assert int(result.developer_summary["commits"].sum()) == 2


def test_analysis_empty_repo(tmp_path):
    empty_path = tmp_path / "empty_repo"
    empty_path.mkdir()
    Repo.init(empty_path)
    result = analyze_repository(str(empty_path))
    assert result.commits.empty
    assert result.developer_summary.empty
    assert result.activity.empty


def test_analysis_invalid_path():
    with pytest.raises(ValueError, match="does not exist or is not a directory"):
        analyze_repository("D:/non_existent_folder_xyz_123")

    with pytest.raises(ValueError, match="Please provide a valid repository path"):
        analyze_repository("")


def test_filter(tmp_path):
    result = analyze_repository(str(make_repo(tmp_path)))
    name = result.commits.iloc[0]["author"]
    filtered = filter_by_developer(result, name)
    assert set(filtered.commits["author"]) == {name}


def test_multi_author_analysis_and_filtering(tmp_path):
    repo_path = make_multi_author_repo(tmp_path)
    result = analyze_repository(str(repo_path))

    # Check overall author extraction
    dev_list = get_developer_list(result)
    assert dev_list == ["Alice", "Bob"]
    assert len(result.commits) == 3

    # Filter by Alice
    alice_res = filter_by_developer(result, "Alice")
    assert len(alice_res.commits) == 2
    assert (alice_res.commits["author"] == "Alice").all()
    assert len(alice_res.developer_summary) == 1
    assert alice_res.developer_summary.iloc[0]["author"] == "Alice"
    assert alice_res.developer_summary.iloc[0]["commits"] == 2

    # Filter by Bob
    bob_res = filter_by_developer(result, "Bob")
    assert len(bob_res.commits) == 1
    assert bob_res.commits.iloc[0]["author"] == "Bob"

    # Filter with 'All developers' returns original result
    all_res = filter_by_developer(result, "All developers")
    assert len(all_res.commits) == 3

    # Filter by non-existent developer
    unknown_res = filter_by_developer(result, "NonExistent")
    assert unknown_res.commits.empty
    assert unknown_res.developer_summary.empty


def test_get_developer_stats(tmp_path):
    repo_path = make_multi_author_repo(tmp_path)
    result = analyze_repository(str(repo_path))

    # All developers stats
    all_stats = get_developer_stats(result, "All developers")
    assert all_stats["commits"] == 3
    assert all_stats["author"] == "All developers"
    assert all_stats["additions"] > 0
    assert all_stats["files_changed"] >= 2

    # Alice stats
    alice_stats = get_developer_stats(result, "Alice")
    assert alice_stats["commits"] == 2
    assert alice_stats["author"] == "Alice"
    assert alice_stats["active_days"] >= 1
    assert alice_stats["net_lines"] > 0
    assert alice_stats["first_commit_date"] != "N/A"

    # Non-existent developer stats
    none_stats = get_developer_stats(result, "Ghost")
    assert none_stats["commits"] == 0
    assert none_stats["additions"] == 0
