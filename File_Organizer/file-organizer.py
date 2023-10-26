import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_name)[1].lower()
            jpg_destination = r"C:\Users\Precious pc\Pictures\download images"
            zip_destination = r"C:\Users\Precious pc\Documents\Zip files"
            png_destination = r"C:\Users\Precious pc\Documents\png_files"
            psd_destination = r"C:\Users\Precious pc\Documents\psd_destination"
            pdf_files = r"C:\Users\Precious pc\Documents\pdf_files"
            other_files = r"C:\Users\Precious pc\Documents\other_files"


            if file_extension == ".jpg":
                shutil.move(file_path , jpg_destination)
            elif file_extension == ".zip":
                shutil.move(file_path, zip_destination)
            elif file_extension == ".png":
                shutil.move(file_path, png_destination)
            elif file_extension == ".psd":
                print(file_extension)
                shutil.move(file_path, psd_destination)
            elif file_extension == ".pdf":
                shutil.move(file_path, pdf_files)
            else:
                shutil.move(file_path, other_files)


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
