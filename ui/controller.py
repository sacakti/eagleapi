"""
UI Controller
Acts as the bridge between the UI and the execution framework.
UI
 │
 ▼
UIController
 │
 ├── Scanner
 ├── Loader
 ├── Runner
 └── Dashboard
"""
from __future__ import annotations
from pathlib import Path
from typing import List, Optional
from framework.loader import RequestLoader
from framework.runner import Runner
from framework.scanner import EndpointScanner
from framework.models import RequestDefinition
from framework.configuration import Configuration

class UIController:
    def __init__(self, context):
        self._context = context
        self._root = Path.cwd()

        self._configuration = Configuration(self._root)

        self._scanner = EndpointScanner(self._root)

        self._loader = RequestLoader(
            self._root
        )
        self._runner = Runner(
            context
        )
        self._endpoints = []
        self._requests = []
        self._selected_endpoint = None
        self._selected_request = None
    # -------------------------------------------------
    # Endpoints
    # -------------------------------------------------
    def load_endpoints(self):
        self._scanner.initialise()
        self._endpoints = self._scanner.scan()
        if self._endpoints:
            self._selected_endpoint = self._endpoints[0]
            self.load_requests(
                self._selected_endpoint.name
            )
        return self._endpoints
    def endpoints(self):
        return self._endpoints
    # -------------------------------------------------
    # Requests
    # -------------------------------------------------
    def load_requests(
        self,
        endpoint_name: str
    ):
        self._requests = self._loader.list_requests(
            endpoint_name
        )
        if self._requests:
            self._selected_request = self._requests[0]
        return self._requests
    def requests(self):
        return self._requests
    # -------------------------------------------------
    # Preview
    # -------------------------------------------------
    def load_request_json(self):
        if (
            self._selected_endpoint is None
            or
            self._selected_request is None
        ):
            return ""
        request = self._loader.load(
            self._selected_endpoint.name,
            self._selected_request
        )
        return request.model_dump_json(
            indent=4,
            by_alias=True
        )
    # -------------------------------------------------
    # Selection
    # -------------------------------------------------
    def select_endpoint(
        self,
        index: int
    ):
        if index < 0:
            return
        if index >= len(self._endpoints):
            return
        self._selected_endpoint = self._endpoints[index]
        self.load_requests(
            self._selected_endpoint.name
        )
    def select_request(
        self,
        index: int
    ):
        if index < 0:
            return
        if index >= len(self._requests):
            return
        self._selected_request = self._requests[index]
    # -------------------------------------------------
    # Execution
    # -------------------------------------------------
    
    def current_request(self):

        if self._selected_endpoint is None:

            return None

        if self._selected_request is None:

            return None

        return self._loader.load(

            self._selected_endpoint.name,

            self._selected_request

        )
 
    def run_all_endpoints(self):
        results = []
        for endpoint in self._endpoints:
            results.extend(
                self._runner.run_all(
                    endpoint.name
                )
            )
        return results
    
    def run_current_request(self):
        # print(f"running controller current request execution")
        if self._selected_endpoint is None:
           return None
        if self._selected_request is None:
           return None
        return self._runner.run_request(
           endpoint=self._selected_endpoint.name,
           request_name=self._selected_request
        )

    def run_current_endpoint(self):
       if self._selected_endpoint is None:
           return []
       return self._runner.run_all(
           self._selected_endpoint.name
       )

    # Save 
    def save_current_request(
        self,
        data
    ):
        if self._selected_endpoint is None:
            return False

        if self._selected_request is None:
            return False

        request = RequestDefinition.model_validate_json(
            data
        )

        self._loader.save(
            endpoint_name=self._selected_endpoint.name,
            request_name=self._selected_request,
            request=request
        )

        return True

    # Create new request
    def create_request(
        self,
        name: str,
        method: str,
        path: str,
    ):
        if self._selected_endpoint is None:
            raise RuntimeError(
                "No endpoint selected."
            )

        request = RequestDefinition(
            name=name,
            method=method,
            path=path,
        )

        self._loader.create(
            endpoint_name=self._selected_endpoint.name,
            request=request,
        )

        # Reload requests from disk
        self.load_requests(
            self._selected_endpoint.name
        )

        return request

    def load_environment(self, environment_name: str):
        self._configuration.load(environment_name)


    def environment_base_url(self) -> str:
        return self._configuration.get("base_url", "")


    def update_environment_base_url(self, base_url: str):
        self._configuration.environment["base_url"] = base_url
        self._configuration.save_environment()

    def available_environments(self):
        return self._configuration.available_environments()

    # -------------------------------------------------
    # Properties
    # -------------------------------------------------
    @property
    def endpoint(self):
        return self._selected_endpoint
    @property
    def request(self):
        return self._selected_request
        