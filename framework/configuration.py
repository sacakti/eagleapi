"""
Loads framework configuration and environment configuration.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict
from framework.constants import Directory
from framework.exceptions import ConfigurationException

class Configuration:
    def __init__(self, root_directory: Path):
        self._root = root_directory
        self._config_directory = root_directory / Directory.CONFIG
        self._framework_configuration = {}
        self._environment_configuration = {}
        
    @property
    def framework(self) -> Dict[str, Any]:
        return self._framework_configuration
    @property
    
    def environment(self) -> Dict[str, Any]:
        return self._environment_configuration
    
    def load(self, environment_name: str) -> None:
        framework_file = self._config_directory / "config.json"
        environment_file = self._config_directory / f"{environment_name}.json"
        self._framework_configuration = self._load_json(framework_file)
        self._environment_configuration = self._load_json(environment_file)
    
    def get(self, key: str, default=None):
        if key in self._environment_configuration:
            return self._environment_configuration[key]
        return self._framework_configuration.get(key, default)
    
    @staticmethod
    def _load_json(file: Path) -> Dict[str, Any]:
        if not file.exists():
            raise ConfigurationException(
                f"Configuration file not found: {file}"
            )
        try:
            with file.open(
                mode="r",
                encoding="utf-8"
            ) as stream:
                return json.load(stream)
        except json.JSONDecodeError as ex:
            raise ConfigurationException(
                f"Invalid JSON : {file}\n{ex}"
            ) from ex