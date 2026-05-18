import os
import hashlib
import zlib

from pygit.repository import (
    OBJECTS_DIR,
    ensure_repo,
)


def hash_content(object_type, content):
    header = f"{object_type} {len(content)}".encode() + b"\0"
    full_data = header + content

    sha1 = hashlib.sha1(full_data).hexdigest()

    return sha1, full_data


def write_object(object_type, content):
    sha1, full_data = hash_content(object_type, content)

    object_dir = os.path.join(OBJECTS_DIR, sha1[:2])
    object_path = os.path.join(object_dir, sha1[2:])

    os.makedirs(object_dir, exist_ok=True)

    compressed = zlib.compress(full_data)

    with open(object_path, "wb") as f:
        f.write(compressed)

    return sha1


def read_object(sha1):
    object_path = os.path.join(OBJECTS_DIR, sha1[:2], sha1[2:])

    with open(object_path, "rb") as f:
        compressed_data = f.read()

    data = zlib.decompress(compressed_data)

    null_index = data.index(b"\0")

    header = data[:null_index].decode()
    content = data[null_index + 1:]

    return header, content


def hash_file_content(filename):
    with open(filename, "rb") as f:
        content = f.read()

    sha1, _ = hash_content("blob", content)

    return sha1


def hash_object(filename):
    ensure_repo()

    with open(filename, "rb") as f:
        content = f.read()

    sha1 = write_object("blob", content)

    return sha1


def hash_object_command(filename):
    print(hash_object(filename))


def cat_file(sha1):
    ensure_repo()

    header, content = read_object(sha1)

    print("HEADER:", header)
    print("CONTENT:")

    try:
        print(content.decode("utf-8"))
    except UnicodeDecodeError:
        print(content)