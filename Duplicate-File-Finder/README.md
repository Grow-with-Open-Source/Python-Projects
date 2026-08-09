# Duplicate File Finder

A command-line tool that scans a directory (recursively) and finds files
that are byte-for-byte identical, based on content hashing rather than
just filenames.

## How it works

1. Files are first grouped by size — files of different sizes can never
   be duplicates, so this is a cheap way to skip most comparisons.
2. Remaining candidates are hashed using SHA-256 (read in chunks, so
   large files don't get loaded into memory all at once).
3. Files that share a hash are reported as duplicates.

## Usage

```bash
python duplicate_finder.py <directory>
```

Example:

```bash
python duplicate_finder.py ~/Downloads
```

Output:

```
Duplicate group (2 files, hash 3a7bd3e2ff...):
  /home/user/Downloads/report.pdf
  /home/user/Downloads/report (1).pdf

Total duplicate groups: 1
Space that could be reclaimed: 245.3 KB
```

### Optional: delete duplicates

```bash
python duplicate_finder.py <directory> --delete
```

This keeps the first file found in each duplicate group and asks for
confirmation before deleting the rest.

## Running tests

```bash
pip install pytest
pytest test_duplicate_finder.py -v
```

## Requirements

None — uses only the Python standard library.
