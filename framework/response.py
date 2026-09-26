"""
Response persistence.
"""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from framework.constants import Directory
from framework.models import ResponseDefinition

class ResponseWriter:
    def __init__(self, root_directory: Path):
        self._response_root = (
            root_directory /
            Directory.ENDPOINTS
        )
    def save(
        self,
        endpoint: str,
        request_name: str,
        response: ResponseDefinition,
        filename: Optional[str] = None
    ) -> Path:
        response_directory = (
            self._response_root /
            endpoint /
            Directory.RESPONSES
        )
        response_directory.mkdir(
            parents=True,
            exist_ok=True
        )
        if filename is None:
            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            filename = (
                f"{endpoint}_"
                f"{request_name}_"
                f"{timestamp}.json"
            )
        file = response_directory / filename
        with file.open(
            "w",
            encoding="utf-8"
        ) as stream:
            json.dump(
                {
                    "statusCode": response.status_code,
                    "elapsedMs": response.elapsed_ms,
                    "sizeBytes": response.size_bytes,
                    "headers": response.headers,
                    "body": response.body
                },
                stream,
                indent=4,
                ensure_ascii=False,
                default=str
            )
        return file