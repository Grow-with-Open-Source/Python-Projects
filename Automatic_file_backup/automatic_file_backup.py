import time
import schedule
import datetime
import shutil
import os

source_dir = ""        # Set this to the folder you want to back up
destination_dir = ""   # Set this to where backups should be saved


def copy_folder_to_directionary(source, dest):
    today = datetime.date.today()
    dest_dir = os.path.join(dest, str(today))

    try:
        shutil.copytree(source, dest_dir)
        print(f"Folder copied to: {dest_dir}")

    except FileExistsError:
        print(f"folderalready exists in {dest}")


schedule.every().day.at("12:00").do(lambda: copy_folder_to_directionary(source_dir, destination_dir)
                                    )

while True:
    schedule.run_pending()
    time.sleep(60)
