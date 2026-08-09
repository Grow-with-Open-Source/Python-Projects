"""Duplicate File Finder.

Scans a directory tree and reports groups of files that are byte-for-byte
identical, based on content hashing rather than filename or size alone.

Usage:
    python duplicate_finder.py <directory> [--delete]

Example:
    python duplicate_finder.py ~/Downloads
    python duplicate_finder.py ~/Downloads --delete
"""

import argparse
import hashlib
import os
from collections import defaultdict


def hash_file(file_path: str, chunk_size: int = 8192) -> str:
    """Return the SHA-256 hash of a file's contents.

    NOTE: files are read in chunks so large files don't get loaded into
    memory all at once.
    """
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicates(root_dir: str) -> dict[str, list[str]]:
    """Walk root_dir and group files by content hash.

    Files are first grouped by size as a cheap pre-filter before hashing,
    since files of different sizes can never be duplicates.
    """
    size_groups: dict[int, list[str]] = defaultdict(list)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                file_size = os.path.getsize(full_path)
            except OSError:
                continue
            size_groups[file_size].append(full_path)

    hash_groups: dict[str, list[str]] = defaultdict(list)
    for candidates in size_groups.values():
        if len(candidates) < 2:
            continue
        for file_path in candidates:
            try:
                file_hash = hash_file(file_path)
            except OSError:
                continue
            hash_groups[file_hash].append(file_path)

    return {h: paths for h, paths in hash_groups.items() if len(paths) > 1}


def print_report(duplicates: dict[str, list[str]]) -> None:
    """Print a human-readable summary of duplicate groups."""
    if not duplicates:
        print('No duplicate files found.')
        return

    total_wasted_bytes = 0
    for file_hash, paths in duplicates.items():
        wasted = os.path.getsize(paths[0]) * (len(paths) - 1)
        total_wasted_bytes += wasted

        print(f'\nDuplicate group ({len(paths)} files, hash {file_hash[:10]}...):')
        for path in paths:
            print(f'  {path}')

    print(f'\nTotal duplicate groups: {len(duplicates)}')
    print(f'Space that could be reclaimed: {total_wasted_bytes / 1024:.1f} KB')


def delete_duplicates(duplicates: dict[str, list[str]]) -> None:
    """Delete all but the first file in each duplicate group."""
    for paths in duplicates.values():
        for path in paths[1:]:
            os.remove(path)
            print(f'Deleted: {path}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Find duplicate files by content.')
    parser.add_argument('directory', help='Directory to scan for duplicates')
    parser.add_argument(
        '--delete',
        action='store_true',
        help='Delete duplicates, keeping only the first file found in each group',
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f'Error: {args.directory} is not a valid directory')
        return

    duplicates = find_duplicates(args.directory)
    print_report(duplicates)

    if args.delete and duplicates:
        confirm = input('\nDelete duplicate files listed above? [y/N]: ')
        if confirm.lower() == 'y':
            delete_duplicates(duplicates)
        else:
            print('Skipped deletion.')


if __name__ == '__main__':
    main()