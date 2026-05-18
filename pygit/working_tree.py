import os
import difflib

from pygit.objects import (
    read_object,
    hash_file_content,
    hash_object,
)

from pygit.index import (
    read_index,
    get_index_entry,
    remove_from_index,
    add_to_index,
)

from pygit.commits import (
    read_tree,
)

from pygit.refs import (
    get_head_commit,
)

from pygit.repository import (
    ensure_repo,
    REPO_DIR,
)


def add(filename):
    ensure_repo()

    sha1 = hash_object(filename)

    add_to_index(filename, sha1)

    print(f"Added {filename}")


def diff(filename):
    ensure_repo()

    sha1 = get_index_entry(filename)

    if not sha1:
        print("File not staged.")
        return

    _, staged_content = read_object(sha1)

    with open(filename, "rb") as f:
        working_content = f.read()

    try:
        staged_text = staged_content.decode("utf-8")
        working_text = working_content.decode("utf-8")

    except UnicodeDecodeError:
        print("Binary or unsupported text encoding.")
        return

    staged_lines = staged_text.splitlines()
    working_lines = working_text.splitlines()

    differences = difflib.unified_diff(
        staged_lines,
        working_lines,
        fromfile="staged",
        tofile="working",
        lineterm=""
    )

    for line in differences:
        print(line)


def status():
    ensure_repo()

    index_entries = read_index()

    committed_entries = {}

    head_commit = get_head_commit()

    if head_commit:
        _, commit_content = read_object(head_commit)

        tree_sha1 = ""

        for line in commit_content.decode().split("\n"):
            if line.startswith("tree "):
                tree_sha1 = line.split(" ")[1]

        if tree_sha1:
            committed_entries = read_tree(tree_sha1)

    working_files = {}

    for filename in os.listdir():
        if filename == REPO_DIR or filename == "main.py":
            continue

        if os.path.isfile(filename):
            working_files[filename] = hash_file_content(filename)

    print("=== Staged Files ===")

    for filename, sha1 in index_entries.items():
        if filename not in committed_entries:
            print(f"new file: {filename}")

        elif committed_entries[filename] != sha1:
            print(f"modified: {filename}")

    print("\n=== Modified Files ===")

    for filename, sha1 in working_files.items():
        if filename in index_entries:
            if index_entries[filename] != sha1:
                print(f"modified: {filename}")

    print("\n=== Untracked Files ===")

    for filename in working_files:
        if filename not in index_entries:
            print(filename)


def rm(filename):
    ensure_repo()

    removed = remove_from_index(filename)

    if not removed:
        print("File not tracked.")
        return

    if os.path.exists(filename):
        os.remove(filename)

    print(f"Removed {filename}")


def restore(filename):
    ensure_repo()

    sha1 = get_index_entry(filename)

    if not sha1:
        print("File not staged.")
        return

    _, blob_content = read_object(sha1)

    with open(filename, "wb") as f:
        f.write(blob_content)

    print(f"Restored {filename}")