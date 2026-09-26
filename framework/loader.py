"""
Loads endpoint request definitions from JSON files.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import List
from pydantic import ValidationError
from framework.constants import Directory
from framework.exceptions import (
   EndpointNotFoundException,
   RequestNotFoundException,
   RequestValidationException,
)
from framework.models import RequestDefinition

class RequestLoader:
    def __init__(self, root_directory: Path):
        self._root_directory = root_directory
        self._endpoint_directory = (
            root_directory / Directory.ENDPOINTS
        )

    def get_endpoint_directory(
        self,
        endpoint_name: str
    ) -> Path:
        endpoint = self._endpoint_directory / endpoint_name
        if not endpoint.exists():
            raise EndpointNotFoundException(
                f"Endpoint '{endpoint_name}' not found."
            )
        return endpoint

    def get_request_directory(
        self,
        endpoint_name: str
    ) -> Path:
        request_directory = (
            self.get_endpoint_directory(endpoint_name)
            / Directory.REQUESTS
        )
        if not request_directory.exists():
            raise RequestNotFoundException(
                f"Request directory not found : {request_directory}"
            )
        return request_directory

    def list_requests(
        self,
        endpoint_name: str
    ) -> List[str]:
        directory = self.get_request_directory(endpoint_name)
        files = sorted(directory.glob("*.json"))
        return [file.stem for file in files]

    def load(
        self,
        endpoint_name: str,
        request_name: str
    ) -> RequestDefinition:
        file = (
            self.get_request_directory(endpoint_name)
            / f"{request_name}.json"
        )
        if not file.exists():
            raise RequestNotFoundException(
                f"Request file not found : {file}"
            )
        return self._load_request(file)

    def load_all(
        self,
        endpoint_name: str
    ) -> List[RequestDefinition]:
        requests = []
        directory = self.get_request_directory(endpoint_name)
        for file in sorted(directory.glob("*.json")):
            requests.append(
                self._load_request(file)
            )
        return requests

    @staticmethod
    def _load_request(
        file: Path
    ) -> RequestDefinition:
        try:
            with file.open(
                "r",
                encoding="utf-8"
            ) as stream:
                data = json.load(stream)
            return RequestDefinition.model_validate(data)
        except ValidationError as ex:
            raise RequestValidationException(
                f"Invalid request definition : {file}\n{ex}"
            ) from ex
        except json.JSONDecodeError as ex:
            raise RequestValidationException(
                f"Invalid JSON : {file}\n{ex}"
           ) from ex