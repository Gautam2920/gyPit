from pygit.objects import read_object

from pygit.commits import read_tree


def collect_reachable_objects(commit_sha1, reachable):
    if not commit_sha1 or commit_sha1 in reachable:
        return

    reachable.add(commit_sha1)

    _, commit_content = read_object(commit_sha1)

    tree_sha1 = ""

    for line in commit_content.decode().split("\n"):
        if line.startswith("tree "):
            tree_sha1 = line.split(" ")[1]

        elif line.startswith("parent "):
            parent_sha1 = line.split(" ")[1]

            if parent_sha1:
                collect_reachable_objects(parent_sha1, reachable)

    if tree_sha1:
        reachable.add(tree_sha1)

        tree_entries = read_tree(tree_sha1)

        for _, blob_sha1 in tree_entries.items():
            reachable.add(blob_sha1)