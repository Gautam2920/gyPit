import os
import zlib

from pygit.commits import read_tree


def read_object_from_repo(repo_path, sha1):
    object_path = os.path.join(
        repo_path,
        ".pygit",
        "objects",
        sha1[:2],
        sha1[2:]
    )

    with open(object_path, "rb") as f:
        compressed_data = f.read()

    data = zlib.decompress(compressed_data)

    null_index = data.index(b"\0")

    header = data[:null_index].decode()
    content = data[null_index + 1:]

    return header, content


def collect_reachable_objects(repo_path, commit_sha1, reachable):
    if not commit_sha1 or commit_sha1 in reachable:
        return

    reachable.add(commit_sha1)

    _, commit_content = read_object_from_repo(
        repo_path,
        commit_sha1
    )

    tree_sha1 = ""

    for line in commit_content.decode().split("\n"):
        if line.startswith("tree "):
            tree_sha1 = line.split(" ")[1]

        elif line.startswith("parent "):
            parent_sha1 = line.split(" ")[1]

            if parent_sha1:
                collect_reachable_objects(
                    repo_path,
                    parent_sha1,
                    reachable
                )

    if tree_sha1:
        reachable.add(tree_sha1)

        tree_entries = read_tree_from_repo(
            repo_path,
            tree_sha1
        )

        for _, blob_sha1 in tree_entries.items():
            reachable.add(blob_sha1)
            
def read_tree_from_repo(repo_path, tree_sha1):
    _, tree_content = read_object_from_repo(
        repo_path,
        tree_sha1
    )

    entries = {}

    for line in tree_content.decode().split("\n"):
        if not line.strip():
            continue

        _, sha1, filename = line.split(" ", 2)

        entries[filename] = sha1

    return entries