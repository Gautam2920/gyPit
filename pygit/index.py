import os

from pygit.repository import INDEX_FILE


def read_index():
    entries = {}

    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            for line in f:
                filename, sha1 = line.strip().split(" ")
                entries[filename] = sha1

    return entries


def write_index(entries):
    with open(INDEX_FILE, "w") as f:
        for filename, sha1 in entries.items():
            f.write(f"{filename} {sha1}\n")


def add_to_index(filename, sha1):
    entries = read_index()

    entries[filename] = sha1

    write_index(entries)


def remove_from_index(filename):
    entries = read_index()

    if filename not in entries:
        return False

    del entries[filename]

    write_index(entries)

    return True


def get_index_entry(filename):
    entries = read_index()

    return entries.get(filename)