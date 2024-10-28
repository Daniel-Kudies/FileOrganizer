"""
JsonLoader module for loading config.json and file_extension.json files.

This module contains the JsonLoader class, which provides methods to
load json files in specified locations.
"""
import json
import logging

class JsonLoader:
    """ Class for loading JSON configuration files.

    This class is responsible for loading configuration settings
    and file extension mappings from JSON files. It provides methods
    to read and parse the JSON data, handling errors related to
    file access and JSON decoding.
    """
    def __init__(self, config_file="config/config.json", file_extensions_config="config/file_extensions.json"):
        self.config_file = config_file
        self.file_extensions_config = file_extensions_config
        self.config = {}
        self.file_extensions = {}

    def load_json(self, file_path):
        """Loads JSON data from the specified file.

        This method reads the content of a JSON file and returns
        the parsed data as a dictionary. If the file cannot be found
        or contains invalid JSON, it logs an error.

        Args:
            file_path (str): The path to the JSON file to load.

        Returns:
            dict: The loaded JSON data if successful, or None if an error occurred.
        """
        try:
            with open(file_path, "r") as x:
                data = json.load(x)
                logging.info("Data from %s loaded successfully.", file_path)
                return data

        except FileNotFoundError:
            logging.error("Configuration file %s not found.", file_path)
        except json.JSONDecodeError:
            logging.error("Error decoding JSON from %s.", file_path)

    def load_config(self):
        self.config = self.load_json(self.config_file)

    def load_file_extensions(self):
        self.file_extensions = self.load_json(self.file_extensions_config)

    def get_config(self):
        return self.config

    def get_file_extensions(self):
        return self.file_extensions
