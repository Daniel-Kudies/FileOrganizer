"""
Main module for the FileOrganizer project.

This module serves as the entry point for the FileOrganizer application.
It initializes the necessary components and triggers the file sorting process.
"""
import logging
import json
from file_sorter import FileSorter

def config_logging():
    """Setup the logging configuration.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler("file_organizer.log"), logging.StreamHandler()])

def main():
    """Main function to run the FileOrganizer.

    Raises:
        FileNotFoundError: If a specified directory is not found.
        PermissionError: If there is a permission issue accessing a directory.
        JSONDecodeError: If there is an error decoding the JSON data.
        Exception: For any other unexpected errors.
    """
    try:
        config_logging()
        logging.info("Start the FileOrganizer...")
        FileSorter().sort_files()
        logging.info("Completed the file sorting.")

    except FileNotFoundError as e:
        logging.error("FileNotFoundError: %s. Please check your file paths.", e)
    except PermissionError as e:
        logging.error("PermissionError: %s. Please check your permissions.", e)
    except json.JSONDecodeError as e:
        logging.error("JSONDecodeError: %s. Please check your JSON files for correctness.", e)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)

if __name__ == "__main__":
    main()
