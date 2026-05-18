import os

from pygit.repository import init_repository

from pygit.refs import (
    set_head,
    is_detached,
)


def test_attached_head(tmp_path):
    os.chdir(tmp_path)

    init_repository()

    set_head("main")

    assert is_detached() is False


def test_detached_head(tmp_path):
    os.chdir(tmp_path)

    init_repository()

    set_head("abc123", detached=True)

    assert is_detached() is True