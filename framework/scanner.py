"""
Workspace and endpoint scanner.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import List
from framework.constants import Directory
from framework.models import EndpointDefinition
class EndpointScanner:
    def __init__(self, root: Path):
        self._root = root
        self._endpoint_root = (
            root / Directory.ENDPOINTS
        )
    # -------------------------------------------------
    def initialise(self):
        """
        Create framework folders if missing.
        """
        for directory in (
            Directory.ENDPOINTS,
            Directory.LOGS,
            Directory.REPORTS,
            Directory.CERTIFICATES,
        ):
            (
                self._root / directory
            ).mkdir(
                parents=True,
                exist_ok=True
            )
    # -------------------------------------------------
    def endpoint_exists(self) -> bool:
        return self._endpoint_root.exists()
    # -------------------------------------------------
    def scan(self) -> List[EndpointDefinition]:
        endpoints = []
        if not self.endpoint_exists():
            return endpoints
        for endpoint in sorted(
            self._endpoint_root.iterdir()
        ):
            if not endpoint.is_dir():
                continue
            requests = endpoint / "requests"
            responses = endpoint / "responses"
            responses.mkdir(
                exist_ok=True
            )
            if not requests.exists():
                continue
            json_files = sorted(
                requests.glob("*.json")
            )
            if not json_files:
                continue
            path = self._discover_path(
                json_files[0]
            )
            endpoints.append(
                EndpointDefinition(
                    name=endpoint.name,
                    path=path,
                    request_count=len(json_files),
                    directory=str(endpoint)
                )
            )
        return endpoints
    # -------------------------------------------------
    @staticmethod
    def _discover_path(
        file: Path
    ) -> str:
        try:
            with file.open(
                encoding="utf-8"
            ) as stream:
                request = json.load(
                    stream
                )
            return request.get(
                "path",
                "-"
            )
        except Exception:
            return "-"
 