# FileOrganizer

**FileOrganizer** is a Python-based utility for organizing files within specified directories, allowing users to sort files by date and by file extension. It runs in the background and is configurable through JSON files.

## Features

- **Sort by Date**: Organizes files into folders by year based on creation date.
- **Sort by Extension**: Organizes files into folders based on file extension categories.
- **Background Operation**: Runs without a user interface and performs tasks quietly.
- **JSON Configuration**: Customizable configuration for directories and file extensions.

## Project Structure

```plaintext
FileOrganizer/
├── config
│   ├── config.json              # Main configuration file
│   └── file_extensions.json     # Defines extensions for different file types
├── file_organizer
│   ├── file_sorter.py           # Contains the main sorting logic
│   ├── json_loader.py           # Loads configurations from JSON files
│   └── main.py                  # Entry point to run the file organizer
├──tests
├── requirements.txt
```

In config/config.json, specify the directories and sorting options:
```json
"directories": {
  "Downloads": {
    "path": "~/Downloads",
      "sorting": {
        "by_date": true,
        "by_extension": true
      }
  }
}
```
In config/file_extensions.json, define file types and extensions:
```json
{
  "Images": [".jpg", ".png", ".gif", ".bmp"],
  "Text": [".txt", ".doc", ".pdf", ".rtf"]
}
```

### Logging:

Logs provide insights into the sorting process, stored in logfile.log.
Logging levels (INFO, DEBUG, ERROR) are adjustable in main.py.

## Code Overview
- **file_sorter.py:** Core logic for organizing files by date and extension. It manages folder creation based on year and file category.
- **json_loader.py:** Manages loading and retrieving JSON configuration data.
- **main.py:** Initializes the sorting process and sets logging configurations.

## Requirements
Python 3.x

## License
This project is open-source. Feel free to modify and adapt it to your needs.
