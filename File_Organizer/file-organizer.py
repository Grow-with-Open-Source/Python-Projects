from pathlib import Path
import shutil
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

CURRENT_WORKING_DIR: Path = Path.cwd()
FILE_TYPES: dict[str, list[str]] = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "videos": [".mp4", ".mkv", ".avi", ".mov"],
    "audio": [".mp3", ".wav", ".flac", ".m4a"],
    "documents": [".pdf", ".docx", ".txt"],
    "archives": [".zip", ".rar", ".7z"],
}
DESTINATION_MAPPING: dict[str, Path] = {
    "images": CURRENT_WORKING_DIR / "Images",
    "videos": CURRENT_WORKING_DIR / "Videos",
    "audio": CURRENT_WORKING_DIR / "Audio Files",
    "documents": CURRENT_WORKING_DIR / "Documents",
    "archives": CURRENT_WORKING_DIR / "Archives",
    "others": CURRENT_WORKING_DIR / "Others"
}

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            file_path: Path = Path(event.src_path)
            file_name: str = file_path.name
            file_extension: str = file_path.suffix.lower()
            category: str = ""

            for category_name, extensions in FILE_TYPES.items():
                if file_extension in extensions:
                    category = category_name
                    break
            else:
                category = "others"

            destination: Path = DESTINATION_MAPPING[category]

            if destination.joinpath(file_name).exists():
                print(f"File {file_name} already exists in the destination. Renaming it")
                count = 1
                while True:
                    if destination.joinpath(f"{file_path.stem}_{count}{file_extension}").exists():
                        count += 1
                    else:
                        destination_path = destination / f"{file_path.stem}_{count}{file_extension}"
                        break
            else:
                destination_path = destination / file_name

            shutil.move(file_path, destination_path)

if __name__ == "__main__":
    folder_to_watch: Path = CURRENT_WORKING_DIR / "monitor"
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_watch, recursive=False)  # Set recursive to True if you want to monitor subdirectories
    observer.start()
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
