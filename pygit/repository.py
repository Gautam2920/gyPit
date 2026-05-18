import os
import sys

REPO_DIR = ".pygit"

OBJECTS_DIR = os.path.join(REPO_DIR, "objects")
REFS_DIR = os.path.join(REPO_DIR, "refs", "heads")
LOGS_DIR = os.path.join(REPO_DIR, "logs")

INDEX_FILE = os.path.join(REPO_DIR, "index")
HEAD_FILE = os.path.join(REPO_DIR, "HEAD")

REMOTES_DIR = os.path.join(
    REPO_DIR,
    "refs",
    "remotes"
)


def repo_exists():
    return os.path.exists(REPO_DIR)


def ensure_repo():
    if not repo_exists():
        print("Not a pygit repository.")
        sys.exit(1)


def init_repository():
    os.makedirs(REPO_DIR, exist_ok=True)
    os.makedirs(OBJECTS_DIR, exist_ok=True)
    os.makedirs(REFS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(REMOTES_DIR, exist_ok=True)

    with open(HEAD_FILE, "w") as f:
        f.write("ref: refs/heads/main")

    with open(os.path.join(LOGS_DIR, "HEAD"), "w") as f:
        pass

    print("Initialized empty pygit repository")