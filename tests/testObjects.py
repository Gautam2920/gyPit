import os

from pygit.objects import (
    hash_content,
    write_object,
    read_object,
)

from pygit.repository import init_repository


def test_hash_content_is_deterministic():
    content = b"hello world"

    sha1_a, _ = hash_content("blob", content)
    sha1_b, _ = hash_content("blob", content)

    assert sha1_a == sha1_b


def test_write_and_read_object(tmp_path):
    os.chdir(tmp_path)

    init_repository()

    content = b"hello world"

    sha1 = write_object("blob", content)

    header, restored_content = read_object(sha1)

    assert header == "blob 11"
    assert restored_content == content