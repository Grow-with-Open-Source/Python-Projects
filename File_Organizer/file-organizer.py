import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        try:
            if not event.is_directory:
                file_path = event.src_path
                file_name = os.path.basename(file_path)
                file_extension = os.path.splitext(file_name)[1].lower()


            try:
                # A dictionary takes file extensions & folder to move each formats to. 
                destination_mapping = {
                    #Key = Format/extension to handle : Value = Folder to move file format. 
                    ".jpg": r"C:\Users\Precious pc\Pictures\download imag",
                    ".zip": r"C:\Users\Precious pc\Documents\Zip files",
                    ".png": r"C:\Users\Precious pc\Documents\png_files",
                    ".psd": r"C:\Users\Precious pc\Documents\psd_destination",
                    ".pdf": r"C:\Users\Precious pc\Documents\pdf_files",
                }
            except ValueError:
                print("folder not found")

                # Default destination for unknown extensions
                other_files = r"C:\Users\Precious pc\Documents\other_files"

                # Get the destination directory for the file extension or use the default
                destination = destination_mapping.get(file_extension, other_files)

                # Move the file to the determined destination
                
                # Check if file already exists in destination & delete it. 
                if os.path.exists(os.path.join(destination, file_name)):
                                print(f"File {file_name} already exists in the destination. Deleting it.")
                                os.remove(os.path.join(destination, file_name))

                            # Move the file to the determined destination
                shutil.move(file_path, destination)
        except ValueError:
            print("an error occur!")

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






          

            
            

