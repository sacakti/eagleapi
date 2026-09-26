"""
HTTP client implementation.
"""
from __future__ import annotations
import time
from typing import Optional
import requests
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, Timeout
from framework.exceptions import HttpRequestException
from framework.models import Environment, RequestDefinition, ResponseDefinition

class HttpClient:
    
    def __init__(self, environment: Environment):
        self._environment = environment
        adapter = HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20
        )
        self._session = Session()
        self._session.mount(
            "http://",
            adapter
        )
        self._session.mount(
            "https://",
            adapter
        )
        self._session.headers.update(
            {
                "User-Agent": "APITest/1.1"
            }
        )
        #
        # TLS Verification
        #
        if environment.verify_ssl:
            self._session.verify = (
                environment.ca_certificate
                if environment.ca_certificate
                else True
            )
        else:
            self._session.verify = False
        #
        # Mutual TLS
        #
        if (
            environment.client_certificate
            and environment.client_key
        ):
            self._session.cert = (
                environment.client_certificate,
                environment.client_key,
            )
            
    @property
    def session(self) -> Session:
        return self._session
    def execute(
        self,
        request: RequestDefinition,
    ) -> ResponseDefinition:
        url = (
            self._environment.base_url.rstrip("/")
            + "/"
            + request.path.lstrip("/")
        )
        start = time.perf_counter()
        try:
            response = self._session.request(
                method=request.method.value,
                url=url,
                headers=request.headers,
                params=request.query,
                json=request.body,
                timeout=(
                    request.timeout
                    if request.timeout is not None
                    else self._environment.timeout
                ),
                allow_redirects=True
            )
        except Timeout as ex:
            raise HttpRequestException(
                f"Request timed out : {url}"
            ) from ex
        except RequestException as ex:
            raise HttpRequestException(
                str(ex)
            ) from ex
        elapsed = (
            time.perf_counter() - start
        ) * 1000
        return ResponseDefinition(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=self._get_body(response),
            elapsed_ms=round(elapsed, 2),
            size_bytes=len(response.content),
            url=url,
            method=request.method.value
        )
        
    @staticmethod
    def _get_body(
        response: requests.Response
    ):
        try:
            return response.json()
        except Exception:
            return response.text

    def close(self):
        self._session.close()