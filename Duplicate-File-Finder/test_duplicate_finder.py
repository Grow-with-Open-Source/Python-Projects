"""Tests for duplicate_finder.py"""

import os
import tempfile

from duplicate_finder import find_duplicates, hash_file


def test_hash_file_is_consistent():
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
        f.write('hello world')
        path = f.name

    try:
        assert hash_file(path) == hash_file(path)
    finally:
        os.remove(path)


def test_find_duplicates_detects_identical_content():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path_a = os.path.join(tmp_dir, 'a.txt')
        path_b = os.path.join(tmp_dir, 'b.txt')
        path_c = os.path.join(tmp_dir, 'c.txt')

        with open(path_a, 'w') as f:
            f.write('same content')
        with open(path_b, 'w') as f:
            f.write('same content')
        with open(path_c, 'w') as f:
            f.write('different content')

        duplicates = find_duplicates(tmp_dir)

        assert len(duplicates) == 1
        (group,) = duplicates.values()
        assert set(group) == {path_a, path_b}


def test_find_duplicates_ignores_unique_files():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with open(os.path.join(tmp_dir, 'a.txt'), 'w') as f:
            f.write('content one')
        with open(os.path.join(tmp_dir, 'b.txt'), 'w') as f:
            f.write('content two')

        duplicates = find_duplicates(tmp_dir)

        assert duplicates == {}


def test_find_duplicates_handles_nested_directories():
    with tempfile.TemporaryDirectory() as tmp_dir:
        nested_dir = os.path.join(tmp_dir, 'nested')
        os.makedirs(nested_dir)

        path_a = os.path.join(tmp_dir, 'a.txt')
        path_b = os.path.join(nested_dir, 'b.txt')

        with open(path_a, 'w') as f:
            f.write('shared content')
        with open(path_b, 'w') as f:
            f.write('shared content')

        duplicates = find_duplicates(tmp_dir)

        assert len(duplicates) == 1
        (group,) = duplicates.values()
        assert set(group) == {path_a, path_b}


def test_find_duplicates_empty_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        assert find_duplicates(tmp_dir) == {}