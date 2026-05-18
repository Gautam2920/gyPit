import os

from pygit.repository import (
    REPO_DIR,
    HEAD_FILE,
    LOGS_DIR,
    OBJECTS_DIR,
    ensure_repo,
)


def get_head_commit():
    with open(HEAD_FILE, "r") as f:
        content = f.read().strip()

    if content.startswith("ref: "):
        ref_path = os.path.join(REPO_DIR, content.split(" ")[1])

        if not os.path.exists(ref_path):
            return None

        with open(ref_path, "r") as ref:
            return ref.read().strip()

    return content


def get_head_ref():
    with open(HEAD_FILE, "r") as f:
        content = f.read().strip()

    if content.startswith("ref: "):
        return os.path.join(REPO_DIR, content.split(" ")[1])

    return None


def is_detached():
    with open(HEAD_FILE, "r") as f:
        return not f.read().startswith("ref: ")


def set_head(value, detached=False):
    with open(HEAD_FILE, "w") as f:
        if detached:
            f.write(value)
        else:
            f.write(f"ref: refs/heads/{value}")


def update_ref(ref_path, new_value):
    old_value = ""

    if os.path.exists(ref_path):
        with open(ref_path, "r") as f:
            old_value = f.read().strip()

    with open(ref_path, "w") as f:
        f.write(new_value)

    os.makedirs(LOGS_DIR, exist_ok=True)

    with open(os.path.join(LOGS_DIR, "HEAD"), "a") as log:
        log.write(f"{old_value} -> {new_value}\n")


def reset(commit_sha1):
    ensure_repo()

    object_path = os.path.join(OBJECTS_DIR, commit_sha1[:2], commit_sha1[2:])

    if not os.path.exists(object_path):
        print("Commit does not exist.")
        return

    update_ref(get_head_ref(), commit_sha1)

    print(f"HEAD reset to {commit_sha1}")


def reflog():
    ensure_repo()

    log_path = os.path.join(LOGS_DIR, "HEAD")

    if not os.path.exists(log_path):
        print("No reflog entries.")
        return

    with open(log_path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(reversed(lines)):
        print(f"{i}: {line.strip()}")