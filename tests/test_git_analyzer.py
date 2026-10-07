from git import Repo
from core.git_analyzer import analyze_repository, validate_repository, filter_by_developer


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


def test_validate_repository(tmp_path):
    path = make_repo(tmp_path)
    assert validate_repository(str(path))
    assert not validate_repository(str(tmp_path / "bad"))


def test_analysis(tmp_path):
    result = analyze_repository(str(make_repo(tmp_path)))
    assert len(result.commits) == 2
    assert int(result.developer_summary["commits"].sum()) == 2


def test_filter(tmp_path):
    result = analyze_repository(str(make_repo(tmp_path)))
    name = result.commits.iloc[0]["author"]
    filtered = filter_by_developer(result, name)
    assert set(filtered.commits["author"]) == {name}
