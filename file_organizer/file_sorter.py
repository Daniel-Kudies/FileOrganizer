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
    """ Class to sort files based on configuration settings.

    The FileSorter class organizes files in specified directories by
    their creation date and file extensions, as defined in the
    configuration. It utilizes a JsonLoader instance to load necessary
    configuration and file extension mappings.
    """
    def __init__ (self):
        json_loader = JsonLoader()
        json_loader.load_config()
        json_loader.load_file_extensions()
        self.config = json_loader.get_config()
        self.file_extensions = json_loader.get_file_extensions()

    def sort_files(self):
        """Sort files in specified directories based on configuration.

        Iterates through the configured directories, logging the process.
        Sorts files either by creation date or by file extension,
        depending on the configuration settings for each directory.

        Raises:
            FileNotFoundError: If a specified directory is not found.
            PermissionError: If there is a permission issue accessing a directory.
            Exception: For any other unexpected errors.
        """
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
        """Sort files in a directory by their extensions.

        Creates folders based on file extensions and moves files into
        these folders. If `bydate` is True, it sorts files into
        year-based folders first, then by extension.

        Args:
            path (str): The directory path where files will be sorted.
            bydate (bool): Flag indicating whether to sort by date first.

        Raises:
            FileNotFoundError: If the specified path is not found.
            PermissionError: If there is a permission issue accessing the path.
            Exception: For any other unexpected errors.
        """
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
        """Sort files in a directory by their creation date.

        Creates year-based folders and moves files into the appropriate
        year folder based on their creation date.

        Args:
            path (str): The directory path where files will be sorted.

        Raises:
            FileNotFoundError: If the specified path is not found.
            PermissionError: If there is a permission issue accessing the path.
            Exception: For any other unexpected errors.
        """
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
        """Create year-based folders in the specified directory.

        Checks for existing folders for each year based on the creation
        dates of the files in the directory. Creates folders for any
        missing years.

        Args:
            path (str): The directory path where year folders will be created.

        Raises:
            FileNotFoundError: If there is an issue accessing the specified path.
            PermissionError: If there is a permission issue creating folders.
            Exception: For any other unexpected errors.
        """
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
                logging.info("Created folder for year: %s in %s", year, path)

        except FileNotFoundError as e:
            logging.error("Error accessing path %s: %s", path, e)
        except PermissionError as e:
            logging.error("PermissionError while creating date folders in %s: %s", path, e)
        except Exception as e:
            logging.error("An unexpected error occurred while creating date folders in %s: %s", path, e)

    def create_extensions_folders(self, path):
        """Create folders for each file extension in the specified directory.

        Checks for existing categories based on file extensions and
        creates folders for each unique category found among the files.

        Args:
            path (str): The directory path where extension folders will be created.

        Raises:
            FileNotFoundError: If there is an issue accessing the specified path.
            PermissionError: If there is a permission issue creating folders.
            Exception: For any other unexpected errors.
        """
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
