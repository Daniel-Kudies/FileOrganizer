"""
Test Class for JsonLoader module for loading config.json and file_extension.json files.

This module contains the tests for the JsonLoader class, which provides methods to
load json files in specified locations.
"""
import json
import logging
import unittest
from unittest.mock import patch, mock_open
from file_organizer.json_loader import JsonLoader

class TestJsonLoader(unittest.TestCase):

    def setUp(self):
        self.loader = JsonLoader(config_file="", extensions_file_config="")

    @patch("builtins.open", new_callable=mock_open, read_data='{"name": "vera"}')
    def test_load_json_success(self, mock_file):
        data = self.loader.load_json("valid_config.json")
        self.assertIsNotNone(data)
        self.assertEqual(data["name"], "vera")
        mock_file.assert_called_once_with("valid_config.json", "r", encoding="utf-8")

    def test_load_json_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.loader.load_json("not_found.json")

    @patch("builtins.open", new_callable=mock_open, read_data='{"invalid":}')
    def test_load_json_invalid(self, mock_open):
        with self.assertRaises(json.JSONDecodeError):
            self.loader.load_json("invalid.json")

if __name__ == '__main__':
    unittest.main()
