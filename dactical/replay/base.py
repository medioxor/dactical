import json
import requests
from typing import Any
import yaml
from pathlib import Path

class Replay:
    """Base class for replay functionality."""

    def __init__(self):
        """Initialize with empty tests list."""
        self.tests = []

    def run(self) -> None:
        for test in self.tests:
            print("Ingesting data for test: ", test["name"])
            attack_data = test["attack_data"][0]
            if "url" == attack_data["type"]:
                self.replay_url(attack_data["data"], attack_data["source"])
            elif "file" == attack_data["type"]:
                self.replay_file(attack_data["data"], attack_data["source"])
            elif "raw" == attack_data["type"]:
                self.replay_data(attack_data["data"], attack_data["source"])
            else:
                raise ValueError("Test must contain 'url', 'file', or 'raw' key")

    def load_test_files(self, directory: str) -> bool:
        """
        Load test data from all YAML files in a directory.
        
        Args:
            directory: Path to directory containing YAML files.
            
        Returns:
            List of test data from all YAML files.
            
        Raises:
            RuntimeError: If YAML parsing fails.
        """
        for file in Path(directory).rglob("*.yaml"):
            try:
                with open(file) as f:
                    data = yaml.safe_load(f)
                    if "tests" in data:
                        self.tests.extend(data["tests"])
            except (yaml.YAMLError, IOError) as e:
                raise RuntimeError(f"Failed to parse {file}: {str(e)}") from e
        
        return True

    def replay_url(self, url: str, source: str) -> Any:
        """
        Replay data from a URL.
        
        Args:
            url: The URL to download the replay data from.
            
        Returns:
            The result of replay_data processing.
            
        Raises:
            RuntimeError: If the download fails.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.text
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to download from {url}: {str(e)}") from e
        
        return self.replay_data(data, source)

    def replay_file(self, path: str, source: str) -> Any:
        """
        Replay data from a file.
        
        Args:
            path: The path to the file containing replay data.
            
        Returns:
            The result of replay_data processing.
            
        Raises:
            RuntimeError: If the file cannot be read.
        """
        try:
            with open(path, 'r') as file:
                data = file.read()
        except IOError as e:
            raise RuntimeError(f"Failed to read file {path}: {str(e)}") from e
        
        return self.replay_data(data, source)

    def replay_data(self, data: str, source: str) -> Any:
        """
        Process the replay data.
        
        Args:
            data: The replay data as a string.
            
        Returns:
            The processed replay data.
            
        Raises:
            NotImplementedError: This is a base method that should be implemented by subclasses.
        """
        raise NotImplementedError("replay_data must be implemented by subclass")