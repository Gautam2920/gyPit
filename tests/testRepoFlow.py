import os

from pygit.repository import init_repository

from pygit.working_tree import add

from pygit.commits import (
    commit,
    log,
    branch,
    switch_branch,
    checkout_commit,
)

from pygit.refs import (
    get_head_commit,
    is_detached,
)


def test_basic_commit_flow(tmp_path, capsys):
    os.chdir(tmp_path)

    init_repository()

    with open("hello.txt", "w") as f:
        f.write("hello world")

    add("hello.txt")

    commit("initial commit")

    head_commit = get_head_commit()

    assert head_commit is not None

    log()

    captured = capsys.readouterr()

    assert "initial commit" in captured.out


def test_branch_creation(tmp_path):
    os.chdir(tmp_path)

    init_repository()

    with open("test.txt", "w") as f:
        f.write("data")

    add("test.txt")

    commit("base commit")

    branch("feature")

    branch_path = os.path.join(
        ".pygit",
        "refs",
        "heads",
        "feature"
    )

    assert os.path.exists(branch_path)


def test_checkout_detached_head(tmp_path):
    os.chdir(tmp_path)

    init_repository()

    with open("a.txt", "w") as f:
        f.write("hello")

    add("a.txt")

    commit("test commit")

    commit_sha1 = get_head_commit()

    checkout_commit(commit_sha1)

    assert is_detached() is True