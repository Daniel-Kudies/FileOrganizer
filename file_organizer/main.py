import logging
from file_sorter import FileSorter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    sorter = FileSorter().sort_files()

if __name__ == "__main__":
    main()