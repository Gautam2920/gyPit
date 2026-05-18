import argparse

from pygit.repository import init_repository

from pygit.objects import (
    hash_object_command,
    cat_file,
)

from pygit.commits import (
    commit,
    log,
    checkout_commit,
    branch,
    switch_branch,
    merge,
    write_tree,
)

from pygit.working_tree import (
    add,
    diff,
    status,
    rm,
    restore,
)

from pygit.refs import (
    reset,
    reflog,
)

from pygit.gc import gc

from pygit.remote import clone_repository

from pygit.remote import (
    clone_repository,
    fetch_repository,
)

from pygit.remote import (
    clone_repository,
    fetch_repository,
    push_repository,
)

from pygit.remote import (
    clone_repository,
    fetch_repository,
    push_repository,
    pull_repository,
)

def main():
    parser = argparse.ArgumentParser(
        prog="pygit",
        description="A miniature Git implementation in Python"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="pygit 1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "init",
        help="Initialize a new pygit repository",
        description="Create a new pygit repository"
    )

    hash_object_parser = subparsers.add_parser(
        "hash-object",
        help="Hash a file into a blob object",
        description="Store a file as a blob object in the object database"
    )

    hash_object_parser.add_argument(
        "filename",
        help="File to hash"
    )

    cat_file_parser = subparsers.add_parser(
        "cat-file",
        help="Display object contents",
        description="Read and display an object from the object database"
    )

    cat_file_parser.add_argument(
        "sha1",
        help="SHA1 hash of object"
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Stage a file",
        description="Add a file to the staging area"
    )

    add_parser.add_argument(
        "filename",
        help="File to stage"
    )

    subparsers.add_parser(
        "write-tree",
        help="Write current index as a tree object",
        description="Create a tree object from the staging area"
    )

    commit_parser = subparsers.add_parser(
        "commit",
        help="Create a new commit",
        description="Create a commit from staged changes"
    )

    commit_parser.add_argument(
        "message",
        help="Commit message"
    )

    subparsers.add_parser(
        "log",
        help="Show commit history",
        description="Display commit history"
    )

    checkout_parser = subparsers.add_parser(
        "checkout",
        help="Checkout a commit",
        description="Checkout a commit in detached HEAD state"
    )

    checkout_parser.add_argument(
        "commit",
        help="Commit hash to checkout"
    )

    branch_parser = subparsers.add_parser(
        "branch",
        help="Create a branch",
        description="Create a new branch"
    )

    branch_parser.add_argument(
        "name",
        help="Branch name"
    )

    switch_parser = subparsers.add_parser(
        "switch",
        help="Switch branches",
        description="Switch to another branch"
    )

    switch_parser.add_argument(
        "name",
        help="Branch name"
    )

    merge_parser = subparsers.add_parser(
        "merge",
        help="Merge branches",
        description="Merge another branch into current branch"
    )

    merge_parser.add_argument(
        "branch",
        help="Branch to merge"
    )

    diff_parser = subparsers.add_parser(
        "diff",
        help="Show file differences",
        description="Compare working tree file against staged version"
    )

    diff_parser.add_argument(
        "filename",
        help="File to compare"
    )

    subparsers.add_parser(
        "status",
        help="Show repository status",
        description="Display working tree status"
    )

    reset_parser = subparsers.add_parser(
        "reset",
        help="Reset HEAD",
        description="Move HEAD to another commit"
    )

    reset_parser.add_argument(
        "commit",
        help="Commit hash"
    )

    subparsers.add_parser(
        "reflog",
        help="Show reflog",
        description="Display HEAD reference history"
    )

    subparsers.add_parser(
        "gc",
        help="Run garbage collection",
        description="Delete unreachable objects"
    )

    rm_parser = subparsers.add_parser(
        "rm",
        help="Remove tracked file",
        description="Remove file from index and working tree"
    )

    rm_parser.add_argument(
        "filename",
        help="File to remove"
    )

    restore_parser = subparsers.add_parser(
        "restore",
        help="Restore file",
        description="Restore file from staging area"
    )

    restore_parser.add_argument(
        "filename",
        help="File to restore"
    )
    
    clone_parser = subparsers.add_parser(
        "clone",
        help="Clone a repository",
        description="Clone a local pygit repository"
    )

    clone_parser.add_argument(
        "source",
        help="Source repository"
    )

    clone_parser.add_argument(
        "destination",
        help="Destination directory"
    )    
    
    fetch_parser = subparsers.add_parser(
        "fetch",
        help="Fetch from remote repository",
        description="Fetch objects and refs from another repository"
    )

    fetch_parser.add_argument(
        "source",
        help="Source repository"
    )

    fetch_parser.add_argument(
        "destination",
        help="Destination repository"
    )    

    push_parser = subparsers.add_parser(
        "push",
        help="Push to remote repository",
        description="Push objects and refs to another repository"
    )

    push_parser.add_argument(
        "source",
        help="Source repository"
    )

    push_parser.add_argument(
        "destination",
        help="Destination repository"
    )

    push_parser.add_argument(
        "--branch",
        default="main",
        help="Branch to push"
    )
    
    pull_parser = subparsers.add_parser(
        "pull",
        help="Pull from remote repository",
        description="Fetch and merge changes from remote repository"
    )

    pull_parser.add_argument(
        "source",
        help="Source repository"
    )

    pull_parser.add_argument(
        "destination",
        help="Destination repository"
    )

    pull_parser.add_argument(
        "--branch",
        default="main",
        help="Branch to pull"
    )

    args = parser.parse_args()

    if args.command == "init":
        init_repository()

    elif args.command == "hash-object":
        hash_object_command(args.filename)

    elif args.command == "cat-file":
        cat_file(args.sha1)

    elif args.command == "add":
        add(args.filename)

    elif args.command == "write-tree":
        write_tree()

    elif args.command == "commit":
        commit(args.message)

    elif args.command == "log":
        log()

    elif args.command == "checkout":
        checkout_commit(args.commit)

    elif args.command == "branch":
        branch(args.name)

    elif args.command == "switch":
        switch_branch(args.name)

    elif args.command == "merge":
        merge(args.branch)

    elif args.command == "diff":
        diff(args.filename)

    elif args.command == "status":
        status()

    elif args.command == "reset":
        reset(args.commit)

    elif args.command == "reflog":
        reflog()

    elif args.command == "gc":
        gc()

    elif args.command == "rm":
        rm(args.filename)

    elif args.command == "restore":
        restore(args.filename)
        
    elif args.command == "clone":
        clone_repository(args.source, args.destination)   
        
    elif args.command == "fetch":
        fetch_repository(
            args.source,
            args.destination
        )
        
    elif args.command == "push":
        push_repository(
            args.source,
            args.destination,
            args.branch
        )   
        
    elif args.command == "pull":
        pull_repository(
            args.source,
            args.destination,
            args.branch
        )  

    else:
        parser.print_help()

if __name__ == "__main__":
    main()