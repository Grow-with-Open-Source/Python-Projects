# Daily Folder Backup

A tiny Python script that automatically backs up a folder to a destination directory once a day, timestamped by date.

## Features

- Runs continuously in the background and triggers a backup every day at a set time
- Copies an entire folder tree using `shutil.copytree`
- Names each backup by the date it was created (e.g. `2026-07-16`), so you get one snapshot per day
- Skips silently (with a message) if a backup for that day already exists, instead of crashing

## Requirements

- Python 3.7+
- [`schedule`](https://pypi.org/project/schedule/) library

Install the dependency with:

```bash
pip install schedule
```

## Configuration

Open the script and set the two path variables at the top:

```python
source_dir = "/path/to/folder/to/back/up"
destination_dir = "/path/to/where/backups/go"
```

By default, the job runs daily at `12:00` (24-hour format). To change the time, edit this line:

```python
schedule.every().day.at("12:00").do(...)
```

## Usage

Run the script and leave it running (e.g. in a terminal, `tmux`/`screen` session, or as a background service):

```bash
python automatic_file_backup.py
```

Each day at the scheduled time, it will create a new folder inside `destination_dir` named after the current date, containing a full copy of `source_dir`.

## How it works

1. `schedule` checks every 60 seconds whether it's time to run the backup job.
2. When triggered, `copy_folder_to_directionary()` builds a destination path using today's date.
3. `shutil.copytree` recursively copies the source folder into that dated destination.
4. If a folder for that date already exists, a `FileExistsError` is caught and a message is printed instead of overwriting or crashing.

## Limitations & ideas for contribution

- Only one backup per day is supported (running twice in a day just logs "already exists")
- No cleanup/rotation of old backups — the destination folder will grow indefinitely
- No logging to a file, only `print` statements
- Could be extended with:
  - Configurable backup retention (e.g. delete backups older than N days)
  - Support for multiple source folders
  - Compression (zip/tar) instead of a raw folder copy
  - A config file or CLI args instead of hardcoded paths
  - Proper logging via Python's `logging` module
