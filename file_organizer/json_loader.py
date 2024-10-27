import json
import logging

class JsonLoader:
    def __init__(self, config_file="config/config.json", file_extensions_config="config/file_extensions.json"):
        self.config_file = config_file
        self.file_extensions_config = file_extensions_config
        self.config = {}
        self.file_extensions = {}

    def load_json(self, file_path):
        try:
            with open(file_path, "r") as x:
                data = json.load(x)
                logging.info(f"Data from {file_path} loaded successfully.")
                return data
            
        except FileNotFoundError:
            logging.error(f"Configuration file {file_path} not found.")
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from {file_path}.")

    def load_config(self):
        self.config = self.load_json(self.config_file)

    def load_file_extensions(self):
        self.file_extensions = self.load_json(self.file_extensions_config)

    def get_config(self):
        return self.config

    def get_file_extensions(self):
        return self.file_extensions