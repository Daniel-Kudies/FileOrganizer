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
    def __init__(self, config_file, extensions_file_config):
        self.config_file = config_file
        self.extensions_file_config = extensions_file_config
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
            dict or None: The loaded JSON data if successful, or None if an error occurred.

        Raises:
            FileNotFoundError: If a specified directory is not found.
            JSONDecodeError: If there is an error decoding the JSON data.
            Exception: For any other unexpected errors.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as x:
                data = json.load(x)
                logging.info("Data from %s loaded successfully.", file_path)
                return data

        except FileNotFoundError:
            logging.error("Configuration file %s not found.", file_path)
            raise
        except json.JSONDecodeError:
            logging.error("Error decoding JSON from %s.", file_path)
            raise
        return None

    def load_config(self):
        """Loads the main configuration from the specified config file.

        This method uses the load_json method to read the main
        configuration file and store the data in the config attribute.
        """
        self.config = self.load_json(self.config_file)

    def load_file_extensions(self):
        """Loads file extensions mapping from the specified file.

        This method uses the load_json method to read the file
        extensions configuration file and store the data in the
        file_extensions attribute.
        """
        self.file_extensions = self.load_json(self.extensions_file_config)

    def get_config(self):
        """Retrieves the loaded configuration data.

        Returns:
            dict: The loaded configuration data.
        """
        return self.config

    def get_file_extensions(self):
        """Retrieves the loaded file extensions data.

        Returns:
            dict: The loaded file extensions data.
        """
        return self.file_extensions
