import os

from pygit.repository import init_repository

from pygit.working_tree import add

from pygit.commits import commit

from pygit.refs import get_head_commit


def test_commit_updates_head(tmp_path):
    os.chdir(tmp_path)

    init_repository()

    with open("hello.txt", "w") as f:
        f.write("hello")

    add("hello.txt")

    commit("first commit")

    head_commit = get_head_commit()

    assert head_commit is not None