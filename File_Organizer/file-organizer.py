import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_name)[1].lower()  # Convert to lowercase

            if file_extension == ".jpg":
                print(f"File extension: {file_extension}")
            else:
                print("None")

if __name__ == "__main__":
    folder_to_watch = r"C:\Users\Precious pc\Documents\file-organizer"  # Replace with the directory you want to monitor
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_watch, recursive=False)  # Set recursive to True if you want to monitor subdirectories
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
