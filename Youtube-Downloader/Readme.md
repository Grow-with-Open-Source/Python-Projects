# YouTube Video Downloader

A small Python script that downloads a YouTube video from a URL you provide, letting you pick the save folder through a native file browser dialog.

## Features

- Prompts for a YouTube URL directly in the terminal
- Opens a native folder-picker dialog (via `tkinter`) so you can choose where the video is saved
- Uses [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) under the hood to handle the actual download, so it benefits from yt-dlp's format support and site compatibility
- Saves the file using the video's title as the filename

## Requirements

- Python 3.7+
- [`yt-dlp`](https://pypi.org/project/yt-dlp/)
- `tkinter` (included with most standard Python installs; on some Linux distros you may need to install it separately, e.g. `sudo apt install python3-tk`)

Install the dependency with:

```bash
pip install yt-dlp
```

## Usage

Run the script:

```bash
python downloader.py
```

You'll be prompted to:

1. Enter the YouTube URL you want to download
2. Choose a destination folder in the dialog that pops up

The video will then download to that folder, named after its title.

## How it works

1. `open_file_dialog()` opens a folder-selection dialog using `tkinter.filedialog.askdirectory()` and returns the chosen path.
2. `download_video()` configures `yt-dlp` with an output template (`%(title)s.%(ext)s`) pointed at that folder and the `"best"` format, then downloads the video.
3. Errors during download (invalid URL, network issues, etc.) are caught and printed rather than crashing the script.

## Limitations & ideas for contribution

- Only supports a single video URL per run (no playlist support)
- Always downloads the `"best"` format — no option to choose resolution, audio-only, or a specific format
- No progress bar; you won't see download progress until it finishes or errors
- No URL validation before attempting the download
- Could be extended with:
  - A simple GUI wrapping the whole flow (not just the folder picker)
  - Format/quality selection (e.g. audio-only extraction)
  - Playlist and batch URL support
  - A progress hook using `yt-dlp`'s `progress_hooks` option
  - Retry logic for transient network failures

## License

MIT (or update to match your project's license).
