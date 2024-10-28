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

"""Class to handle file sorting based on configurations loaded from JSON."""
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
                logging.info(f"Processing directory: {directory}")

                path = os.path.expanduser(details.get("path", ""))
                sortingoptions = details.get("sorting", {})

                if sortingoptions.get("by_date"):
                    self.sort_file_date(path)
                if sortingoptions.get("by_extension"):
                    self.sort_file_extensions(path, sortingoptions.get("by_date"))

        except FileNotFoundError as e:
            logging.error(f"File sorting error: {e}")
        except PermissionError as e:
            logging.error(f"PermissionError: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def sort_file_extensions(self, path, bydate):
        try:
            logging.debug(f"Sorting by File Extensions in Directory: {path}")

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
                                        logging.info(f"Moved file {file.name} to {targetfolder}")

            for file in os.scandir(path):
                if file.is_file():
                    extension = os.path.splitext(file.name)[1]
                    for category, extensions in self.file_extensions.items():
                        if extension in extensions:
                            targetfolder = os.path.join(path, category)
                            os.makedirs(targetfolder, exist_ok=True)
                            shutil.move(file.path, os.path.join(targetfolder, file.name))
                            logging.info(f"Moved file {file.name} to {targetfolder}")


        except FileNotFoundError as e:
            logging.error(f"File not found error: {e}")
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def sort_file_date(self, path):
        try:
            logging.debug(f"Sorting by File Date in Directory: {path}")
 
            self.create_date_folder(path)

            for file in os.scandir(path):
                if file.is_file():
                    temp = os.path.getctime(file)
                    creationtime = datetime.datetime.fromtimestamp(temp).year
                    shutil.move(file.path, os.path.join(os.path.join(path, str(creationtime)), file.name))
                    logging.info(f"Sorted File {file.name} in {path}{str(creationtime)}{file.name}")

        except FileNotFoundError as e:
            logging.error(f"File not found error: {e}")
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def create_date_folder(self, path):
        try:
            logging.debug(f"Looking for Folder in Directory: {path} if they exists do nothing else create it")
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
            logging.error(f"Error accessing path {path}: {e}")
        except PermissionError as e:
            logging.error(f"PermissionError while creating date folders in {path}: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while creating date folders in {path}: {e}")

    def create_extensions_folders(self, path):
        try:
            logging.debug(f"Creating Extension Folders in Directory: {path} if they exists do nothing else create it")

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
                logging.info(f"Created folder for category: {category} in {path}")

        except FileNotFoundError as e:
            logging.error(f"Error accessing path {path}: {e}")
        except PermissionError as e:
            logging.error(f"PermissionError while creating date folders in {path}: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while creating date folders in {path}: {e}")
