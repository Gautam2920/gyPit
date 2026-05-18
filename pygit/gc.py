import os

from pygit.objects import read_object

from pygit.commits import read_tree

from pygit.repository import (
    ensure_repo,
    OBJECTS_DIR,
    REFS_DIR,
)

from pygit.graph import collect_reachable_objects

def gc():
    ensure_repo()

    reachable = set()

    for branch in os.listdir(REFS_DIR):
        branch_path = os.path.join(REFS_DIR, branch)

        with open(branch_path, "r") as f:
            commit_sha1 = f.read().strip()

        collect_reachable_objects(commit_sha1, reachable)

    deleted = 0

    for subdir in os.listdir(OBJECTS_DIR):
        subdir_path = os.path.join(OBJECTS_DIR, subdir)

        if not os.path.isdir(subdir_path):
            continue

        for filename in os.listdir(subdir_path):
            sha1 = subdir + filename

            if sha1 not in reachable:
                os.remove(os.path.join(subdir_path, filename))
                deleted += 1

    print(f"Garbage collection complete. Deleted {deleted} objects.")