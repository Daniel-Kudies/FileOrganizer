"""
FileSorter module for organizing files by date and extensions.

This module contains the FileSorter class, which provides methods to
sort files in specified directories based on configuration settings
such as sorting by date or extension.
"""
import os
import shutil
import logging
import datetime
from json_loader import JsonLoader

class FileSorter:
    def __init__ (self):
        json_loader = JsonLoader()
        json_loader.load_config()
        json_loader.load_file_extensions()
        self.config = json_loader.get_config()
        self.file_extensions = json_loader.get_file_extensions()

    def sort_files(self):
        try:
            for directory, details in self.config.get("directories", {}).items():
                logging.info("Processing directory: %s", {directory})

                path = os.path.expanduser(details.get("path", ""))
                sortingoptions = details.get("sorting", {})

                if sortingoptions.get("by_date"):
                    self.sort_file_date(path)
                if sortingoptions.get("by_extension"):
                    self.sort_file_extensions(path, sortingoptions.get("by_date"))

        except FileNotFoundError as e:
            logging.error("File sorting error: %s", e)
        except PermissionError as e:
            logging.error("PermissionError: %s", e)
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)

    def sort_file_extensions(self, path, bydate):
        try:
            logging.debug("Sorting by File Extensions in Directory: %s", path)

            self.create_extensions_folders(path)
            if bydate:
                logging.info("Sorting by extensions within date folders.")

                for year_folder in os.scandir(path):
                    if year_folder.is_dir():
                        year_path = os.path.join(path, year_folder.name)
                        self.create_extensions_folders(year_path)

                        for file in os.scandir(year_path):
                            if file.is_file():
                                extension = os.path.splitext(file.name)[1]
                                for category, extensions in self.file_extensions.items():
                                    if extension in extensions:
                                        targetfolder = os.path.join(year_path, category)
                                        os.makedirs(targetfolder, exist_ok=True)
                                        shutil.move(file.path, os.path.join(targetfolder, file.name))
                                        logging.info("Moved file %s to %s", file.name, targetfolder)

            for file in os.scandir(path):
                if file.is_file():
                    extension = os.path.splitext(file.name)[1]
                    for category, extensions in self.file_extensions.items():
                        if extension in extensions:
                            targetfolder = os.path.join(path, category)
                            os.makedirs(targetfolder, exist_ok=True)
                            shutil.move(file.path, os.path.join(targetfolder, file.name))
                            logging.info("Moved file %s to %s", file.name, targetfolder)

        except FileNotFoundError as e:
            logging.error("File not found error: %s", e)
        except PermissionError as e:
            logging.error("Permission denied: %s", e)
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)

    def sort_file_date(self, path):
        try:
            logging.debug("Sorting by File Date in Directory: %s", path)

            self.create_date_folder(path)

            for file in os.scandir(path):
                if file.is_file():
                    temp = os.path.getctime(file)
                    creationtime = datetime.datetime.fromtimestamp(temp).year
                    shutil.move(file.path, os.path.join(os.path.join(path, str(creationtime)), file.name))
                    logging.info("Sorted File %s in %s%s%s", file.name, path, str(creationtime), file.name)

        except FileNotFoundError as e:
            logging.error("File not found error: %s", {e})
        except PermissionError as e:
            logging.error("Permission denied: %s", {e})
        except Exception as e:
            logging.error("An unexpected error occurred: %s", {e})

    def create_date_folder(self, path):
        try:
            logging.debug("Looking for Folder in Directory: %s if they exist, do nothing; else create it", path)
            time = []

            for file in os.scandir(path):
                if file.is_file():
                    temp = os.path.getctime(file)
                    time.append(datetime.datetime.fromtimestamp(temp).year)

            time = list(set(time))

            for year in time:
                os.makedirs(os.path.join(path, str(year)), exist_ok=True)
                logging.info(f"Created folder for year: {year} in {path}")

        except FileNotFoundError as e:
            logging.error("Error accessing path %s: %s", path, e)
        except PermissionError as e:
            logging.error("PermissionError while creating date folders in %s: %s", path, e)
        except Exception as e:
            logging.error("An unexpected error occurred while creating date folders in %s: %s", path, e)

    def create_extensions_folders(self, path):
        try:
            logging.debug("Creating Extension Folders in Directory: %s if they exist, do nothing; else create it", path)

            existing_extensions = set()

            for file in os.scandir(path):
                if file.is_file():
                    extension = os.path.splitext(file.name)[1]
                    for category, extensions in self.file_extensions.items():
                        if extension in extensions:
                            existing_extensions.add(category)

            for category in existing_extensions:
                targetfolder = os.path.join(path, category)
                os.makedirs(targetfolder, exist_ok=True)
                logging.info("Created folder for category: %s in %s", category, path)

        except FileNotFoundError as e:
            logging.error("Error accessing path %s: %s", path, e)
        except PermissionError as e:
            logging.error("PermissionError while creating date folders in %s: %s", path, e)
        except Exception as e:
            logging.error("An unexpected error occurred while creating date folders in %s: %s", path, e)
