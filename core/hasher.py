import hashlib
import os
from collections import defaultdict

def get_file_hash(filepath: str, chunk_size: int = 65536) -> str:
    """Compute SHA-256 hash of a file using buffered reading."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(directory: str) -> dict[str, list[str]]:
    """Group files by (size, sha256) to detect exact duplicates in O(N) time."""
    # Optimization 1: Group by file size first to avoid hashing unique sizes
    size_map = defaultdict(list)
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.startswith("."):
                continue
            full_path = os.path.join(root, filename)
            try:
                size_map[os.path.getsize(full_path)].append(full_path)
            except OSError:
                continue

    # Optimization 2: Only compute SHA-256 for files sharing identical byte sizes
    duplicates = {}
    for size, paths in size_map.items():
        if len(paths) < 2:
            continue
        hash_map = defaultdict(list)
        for path in paths:
            try:
                file_hash = get_file_hash(path)
                hash_map[file_hash].append(path)
            except OSError:
                continue
        for file_hash, matched_paths in hash_map.items():
            if len(matched_paths) > 1:
                duplicates[file_hash] = matched_paths

    return duplicates
