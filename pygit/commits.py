import os
import time

from pygit.objects import (
    write_object,
    read_object,
)

from pygit.refs import (
    get_head_commit,
    get_head_ref,
    is_detached,
    set_head,
    update_ref,
)

from pygit.index import read_index

from pygit.repository import (
    ensure_repo,
    REFS_DIR,
)


def write_tree_internal():
    entries = []

    index_entries = read_index()

    if not index_entries:
        print("Nothing staged.")
        return None

    for filename, sha1 in index_entries.items():
        entries.append(f"blob {sha1} {filename}")

    tree_content = "\n".join(entries).encode()

    tree_sha1 = write_object("tree", tree_content)

    return tree_sha1


def write_tree():
    ensure_repo()

    tree_sha1 = write_tree_internal()

    if tree_sha1:
        print(tree_sha1)


def read_tree(tree_sha1):
    _, tree_content = read_object(tree_sha1)

    entries = {}

    for line in tree_content.decode().split("\n"):
        if not line.strip():
            continue

        _, sha1, filename = line.split(" ", 2)

        entries[filename] = sha1

    return entries


def restore_working_tree_from_commit(commit_sha1):
    _, commit_content = read_object(commit_sha1)

    tree_sha1 = ""

    for line in commit_content.decode().split("\n"):
        if line.startswith("tree "):
            tree_sha1 = line.split(" ")[1]

    _, tree_content = read_object(tree_sha1)

    for line in tree_content.decode().split("\n"):
        if not line.strip():
            continue

        _, blob_sha1, filename = line.split(" ", 2)

        _, blob_content = read_object(blob_sha1)

        with open(filename, "wb") as f:
            f.write(blob_content)


def commit(message):
    ensure_repo()

    tree_sha1 = write_tree_internal()

    if not tree_sha1:
        return

    parent = get_head_commit() or ""

    commit_content = f"""tree {tree_sha1}
parent {parent}
date {int(time.time())}

{message}
""".encode()

    commit_sha1 = write_object("commit", commit_content)

    if is_detached():
        set_head(commit_sha1, detached=True)
    else:
        update_ref(get_head_ref(), commit_sha1)

    print(commit_sha1)


def log():
    ensure_repo()

    current_commit = get_head_commit()

    if not current_commit:
        print("No commits yet.")
        return

    while current_commit:
        _, content = read_object(current_commit)

        text = content.decode()

        print("=" * 50)
        print("Commit:", current_commit)
        print(text)

        parents = []

        for line in text.split("\n"):
            if line.startswith("parent "):
                value = line.split(" ", 1)[1]

                if value:
                    parents.append(value)

        current_commit = parents[0] if parents else ""


def checkout_commit(commit_sha1):
    ensure_repo()

    restore_working_tree_from_commit(commit_sha1)

    set_head(commit_sha1, detached=True)

    print("HEAD detached at", commit_sha1)


def branch(branch_name):
    ensure_repo()

    current_commit = get_head_commit()

    branch_path = os.path.join(REFS_DIR, branch_name)

    with open(branch_path, "w") as f:
        f.write(current_commit)

    print(f"Created branch '{branch_name}'")


def switch_branch(branch_name):
    ensure_repo()

    branch_path = os.path.join(REFS_DIR, branch_name)

    if not os.path.exists(branch_path):
        print("Branch does not exist.")
        return

    with open(branch_path, "r") as f:
        commit_sha1 = f.read().strip()

    restore_working_tree_from_commit(commit_sha1)

    set_head(branch_name)

    print(f"Switched to branch '{branch_name}'")


def merge(branch_name):
    ensure_repo()

    if "/" in branch_name:
        branch_path = os.path.join(
            ".pygit",
            "refs",
            "remotes",
            branch_name
        )
    else:
        branch_path = os.path.join(
            REFS_DIR,
            branch_name
        )

    if not os.path.exists(branch_path):
        print("Branch does not exist.")
        return

    with open(branch_path, "r") as f:
        merge_commit = f.read().strip()

    current_commit = get_head_commit()

    tree_sha1 = write_tree_internal()

    commit_content = f"""tree {tree_sha1}
parent {current_commit}
parent {merge_commit}
date {int(time.time())}

Merge branch '{branch_name}'
""".encode()

    commit_sha1 = write_object("commit", commit_content)

    update_ref(get_head_ref(), commit_sha1)

    print("Merged successfully.")
    print(commit_sha1)