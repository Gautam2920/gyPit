import os
import socket
import json

from pygit.refs import get_head_commit

from pygit.objects import read_object

from pygit.commits import read_tree


def get_latest_files():
    head_commit = get_head_commit()

    if not head_commit:
        print("No commits found.")
        return {}

    _, commit_content = read_object(head_commit)

    tree_sha1 = ""

    for line in commit_content.decode().split("\n"):
        if line.startswith("tree "):
            tree_sha1 = line.split(" ")[1]

    entries = read_tree(tree_sha1)

    files = {}

    for filename, blob_sha1 in entries.items():
        _, blob_content = read_object(blob_sha1)

        try:
            files[filename] = blob_content.decode("utf-8")
        except UnicodeDecodeError:
            continue

    return files


def deploy(ip, port=9000):
    files = get_latest_files()

    if not files:
        return

    payload = json.dumps(files)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((ip, port))

    client.sendall(payload.encode())

    response = client.recv(1024).decode()

    print(response)

    client.close()