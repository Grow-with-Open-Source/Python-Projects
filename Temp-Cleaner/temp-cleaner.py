#!/usr/bin/env python

import os
import sys
import logging
import argparse
from datetime import datetime
import platform


class ProgressBar:
    def __init__(self, total, *, prefix='Progress:', suffix='Completed', width=50, fill='=', empty=' '):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.width = width
        self.fill = fill
        self.empty = empty
        self.current = 0

    def calculate_progress(self):
        try:
            progress = min(float(self.current) / self.total, 1.0)
        except ZeroDivisionError:
            progress = 1.0

        filled = int(self.width * progress)
        bar = f'{self.fill * filled}{self.empty * (self.width - filled)}'
        percent = int(progress * 100)
        output_str = f'\r{self.prefix} [{bar}] {percent}% ({self.current}/{self.total}) {self.suffix}'

        if self.current >= self.total:
            output_str += '\n'
        return output_str

    def print(self):
        sys.stdout.write(self.calculate_progress())
        sys.stdout.flush()

    def update(self, count=1):
        self.current = min(self.current + count, self.total)
        self.print()

    def finish(self):
        self.current = self.total
        self.print()


class Logger:
    __levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    __default_log_filename = f"temp_cleaner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    __default_log_format = "%(asctime)s [%(levelname)s]: %(message)s"

    def __init__(self):
        self.logger = logging.getLogger("TempCleaner")
        self.logger.setLevel(logging.INFO)
        self.handlers = []
        self.logger.propagate = False                       # Prevent duplicate logging

    def add_handler(self, handler):
        handler.setFormatter(logging.Formatter(self.__default_log_format))
        self.handlers.append(handler)
        self.logger.addHandler(handler)

    def clear_handlers(self):
        for handler in self.handlers:
            handler.flush()
            self.logger.removeHandler(handler)
            handler.close()
        self.handlers.clear()

    def __del__(self):
        self.clear_handlers()

    def __file_handler_logic(self, log_filename):
        log_file = log_filename if log_filename else self.__default_log_filename
        try:
            file_handler = logging.FileHandler(log_file)
            self.add_handler(file_handler)
        except (PermissionError, OSError) as e:
            self.logger.error(
                f"Failed to create log file '{log_file}': {e}")
            # Attempt to create in current directory as fallback
            if log_filename:
                fallback_file = os.path.basename(log_file)
                try:
                    file_handler = logging.FileHandler(fallback_file)
                    self.add_handler(file_handler)
                    self.logger.warning(
                        f"Using fallback log file: {fallback_file}")
                except Exception as e:
                    self.logger.error(
                        f"Failed to create fallback log file: {e}")

    def configure(self, log_level='INFO', save_log=False, log_filename=None, silent=False):
        # Clean up existing handlers
        self.clear_handlers()

        try:
            # Set log level
            level = self.__levels.get(log_level.upper(), logging.INFO)
            self.logger.setLevel(level)

            # Silent mode: use NullHandler
            if silent:
                self.add_handler(logging.NullHandler())
                return self

            # Add console handler by default unless silent
            self.add_handler(logging.StreamHandler())

            # Handle file logging
            if save_log or log_filename:
                self.__file_handler_logic(log_filename)

        except Exception as e:
            self.logger.error(f"Failed to configure logger: {e}")

        finally:
            # Ensure we have at least a NullHandler
            if not self.handlers:
                self.add_handler(logging.NullHandler())

        return self

    def get_logger(self):
        return self.logger


class ArgsParser:
    DEFAULT_CONFIG = {
        '--log-level':  {
            'type': str,
            'default': 'INFO',
            'help': 'Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)'
        },
        '--save-log': {
            'action': 'store_true',
            'help': 'Save log to a file'
        },
        '--log-filename': {
            'type': str,
            'help': 'Specify log filename'
        },
        '--silent': {
            'action': 'store_true',
            'help': 'Show only the progress without logging details'
        }
    }

    def __init__(self):
        description="Temp Files Cleaner that cleans temporary files from system temp directories."
        self.parser = argparse.ArgumentParser(description=description)
        for arg, params in self.DEFAULT_CONFIG.items():
            self.parser.add_argument(arg, **params)

    def parse(self):
        return self.parser.parse_args()


def does_path_exist(path):
    return path is not None and os.path.exists(path)

def get_temp_directories():
    temp_dirs = [
        os.environ.get('TEMP'),
        os.environ.get('TMP')
    ]

    match platform.system():
        case 'Windows':          # Windows
            temp_dirs.extend([
                os.path.join('C:', 'Windows', 'Temp'),
                os.path.join('C:', 'Windows', 'Prefetch'),
                os.path.join('C:', 'Users', os.getlogin(), 'AppData', 'Local', 'Temp')
            ])
        case 'Darwin':           # macOS
            temp_dirs.extend([
                os.path.join(os.path.expanduser('~'), 'Library', 'Caches'),
                '/private/var/folders',
                '/private/var/tmp',
                '/private/tmp'
            ])
        case 'Linux':            # Any Linux Distro
            temp_dirs.extend([
                '/tmp',
                '/var/tmp',
                os.path.join(os.path.expanduser('~'), '.cache')
            ])

    return list(filter(does_path_exist, temp_dirs))


def delete_directory_contents(path, logger=None, progress_bar=None):
    deleted, skipped = 0, 0

    if logger is None:
        logger = logging.getLogger(__name__)

    if not does_path_exist(path):
        logger.warning(f"Directory not found: {path}")
        return deleted, skipped

    if os.path.isdir(path):
        try:
            # Safely get directory contents
            items = os.listdir(path)
        except PermissionError as e:
            logger.warning(f"Permission denied accessing directory: {path} | Reason: {e}")
            skipped += 1
            if progress_bar:
                progress_bar.update()
            return deleted, skipped
        except OSError as e:
            logger.error(f"OS error accessing directory: {path} | Reason: {e}")
            skipped += 1
            if progress_bar:
                progress_bar.update()
            return deleted, skipped

        # Process directory contents
        for item in items:
            try:
                item_path = os.path.join(path, item)
                recursive_deleted, recursive_skipped = delete_directory_contents(
                    item_path,
                    logger,
                    progress_bar
                )
                deleted += recursive_deleted
                skipped += recursive_skipped
            except OSError as e:
                logger.error(f"Error processing path: {item_path} | Reason: {e}")
                skipped += 1
                if progress_bar:
                    progress_bar.update()
    else:
        try:
            os.remove(path)
            logger.info(f"Deleted file: {path}")
            deleted += 1
        except PermissionError as e:
            logger.warning(f"File in use: {path} | Reason: {e}")
            skipped += 1
        except OSError as e:
            logger.error(f"OS error deleting file: {path} | Reason: {e}")
            skipped += 1

    if progress_bar:
        progress_bar.update()

    return deleted, skipped


def total_file_counter(directory):
    total_files = 0
    try:
        for root, dirs, files in os.walk(directory):
            total_files += len(files) + len(dirs)
        return total_files
    except (FileNotFoundError, PermissionError, OSError):
        return 0


def execute_temp_cleaning(directory_list, cmd_args, logger_instance, progress_bar):
    logger = logger_instance.configure(**vars(cmd_args)).get_logger()

    if progress_bar:
        progress_bar.print()

    logger.info("---- Starting safe cleaning of temp directories ----")

    for temp_dir in directory_list:
        logger.info(f"Cleaning directory: {temp_dir}")
        deleted, skipped = delete_directory_contents(
            temp_dir,
            logger,
            progress_bar
        )
        logger.info(
            f"Summary for {temp_dir}: Deleted: {deleted}, Skipped: {skipped}")

    if progress_bar:
        progress_bar.finish()

    logger.info("---- Cleaning completed. Check log for details. ----")


def main():
    args_parser = ArgsParser()
    logger_instance = Logger()

    directory_list = get_temp_directories()
    cmd_args = args_parser.parse()

    total_temp_files_count = sum(map(total_file_counter, directory_list))
    progress_bar = ProgressBar(total_temp_files_count)

    execute_temp_cleaning(
        directory_list,
        cmd_args,
        logger_instance,
        progress_bar
    )


if __name__ == "__main__":
    main()
