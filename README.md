# pyGit

A miniature Git implementation built in Python.

This project was created to deeply understand how Git works internally by rebuilding core Git concepts from scratch step by step.

pyGit is not intended to replace Git itself.  
It is an educational distributed version control system that demonstrates:

- content-addressed object storage
- blobs, trees, and commits
- branches and refs
- detached HEAD state
- staging/index system
- commit graph traversal
- merging
- garbage collection
- repository cloning
- fetch / push / pull
- remote tracking references

---

# Features

## Repository

- Initialize repositories
- Repository metadata management
- HEAD and refs handling

## Objects

- Blob storage
- Tree objects
- Commit objects
- SHA1 content-addressed storage
- Object compression using zlib

## Working Tree

- Add files
- Remove files
- Restore files
- Diff staged vs working tree
- Repository status

## Commits

- Create commits
- Commit history traversal
- Branching
- Checkout commits
- Merge branches

## Distributed Features

- Clone repositories
- Fetch objects and refs
- Push branches
- Pull remote changes

## Maintenance

- Reflog
- Garbage collection
- Reachability traversal

---

# Project Structure

```text
pyGit/
│
├── main.py
│
├── pygit/
│   ├── __init__.py
│   ├── repository.py
│   ├── objects.py
│   ├── refs.py
│   ├── index.py
│   ├── commits.py
│   ├── working_tree.py
│   ├── graph.py
│   ├── remote.py
│   └── gc.py
│
├── tests/
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Gautam2920/gyPit
cd pyGit
```

Install dependencies:

```bash
pip install pytest
```

---

# Usage

Initialize repository:

```bash
python main.py init
```

Add files:

```bash
python main.py add hello.txt
```

Commit changes:

```bash
python main.py commit "initial commit"
```

View history:

```bash
python main.py log
```

Check repository status:

```bash
python main.py status
```

Create branch:

```bash
python main.py branch feature
```

Switch branch:

```bash
python main.py switch feature
```

Merge branch:

```bash
python main.py merge main
```

Clone repository:

```bash
python main.py clone repoA repoB
```

Fetch changes:

```bash
python main.py fetch repoA repoB
```

Push changes:

```bash
python main.py push repoA repoB
```

Pull changes:

```bash
python main.py pull repoA repoB
```

---

# Testing

Run all tests:

```bash
pytest
```

---
