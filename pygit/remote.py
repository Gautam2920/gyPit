import os
import shutil

from pygit.repository import REPO_DIR

from pygit.refs import get_head_commit

from pygit.commits import restore_working_tree_from_commit

from pygit.graph import collect_reachable_objects

from pygit.repository import (
    OBJECTS_DIR,
    REFS_DIR,
)

from pygit.repository import (
    REMOTES_DIR,
)

from pygit.refs import get_head_commit

from pygit.commits import merge

def clone_repository(source, destination):
    source_repo = os.path.join(source, REPO_DIR)

    if not os.path.exists(source_repo):
        print("Source repository does not exist.")
        return

    if os.path.exists(destination):
        print("Destination already exists.")
        return

    os.makedirs(destination)

    destination_repo = os.path.join(destination, REPO_DIR)

    shutil.copytree(source_repo, destination_repo)

    current_dir = os.getcwd()

    os.chdir(destination)

    head_commit = get_head_commit()

    if head_commit:
        restore_working_tree_from_commit(head_commit)

    os.chdir(current_dir)

    print(f"Cloned repository from '{source}' to '{destination}'")
    
def fetch_objects(source, destination):
    reachable = set()

    for branch in os.listdir(
        os.path.join(source, REFS_DIR)
    ):
        branch_path = os.path.join(
            source,
            REFS_DIR,
            branch
        )

        with open(branch_path, "r") as f:
            commit_sha1 = f.read().strip()

        collect_reachable_objects(commit_sha1, reachable)

    copied = 0

    for sha1 in reachable:
        source_object = os.path.join(
            source,
            OBJECTS_DIR,
            sha1[:2],
            sha1[2:]
        )

        destination_dir = os.path.join(
            destination,
            OBJECTS_DIR,
            sha1[:2]
        )

        destination_object = os.path.join(
            destination_dir,
            sha1[2:]
        )

        if not os.path.exists(destination_object):
            os.makedirs(destination_dir, exist_ok=True)

            shutil.copy2(source_object, destination_object)

            copied += 1

    print(f"Fetched {copied} objects.")
    
def fetch_refs(source, destination, remote_name="origin"):
    source_heads = os.path.join(
        source,
        REFS_DIR
    )

    destination_remote = os.path.join(
        destination,
        REMOTES_DIR,
        remote_name
    )

    os.makedirs(destination_remote, exist_ok=True)

    for branch in os.listdir(source_heads):
        source_branch = os.path.join(
            source_heads,
            branch
        )

        destination_branch = os.path.join(
            destination_remote,
            branch
        )

        shutil.copy2(
            source_branch,
            destination_branch
        )

    print(f"Fetched remote refs from '{remote_name}'")
    
def fetch_repository(source, destination):
    fetch_objects(source, destination)

    fetch_refs(source, destination)

    print("Fetch complete.")
    
def push_repository(source, destination, branch="main"):
    fetch_objects(source, destination)

    source_branch = os.path.join(
        source,
        REFS_DIR,
        branch
    )

    destination_branch = os.path.join(
        destination,
        REFS_DIR,
        branch
    )

    if not os.path.exists(source_branch):
        print("Source branch does not exist.")
        return

    os.makedirs(
        os.path.dirname(destination_branch),
        exist_ok=True
    )

    shutil.copy2(
        source_branch,
        destination_branch
    )

    print(f"Pushed branch '{branch}'")
    
def pull_repository(source, destination, branch="main"):
    fetch_repository(source, destination)

    current_dir = os.getcwd()

    os.chdir(destination)

    merge(f"origin/{branch}")

    os.chdir(current_dir)

    print("Pull complete.")