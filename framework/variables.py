"""
Variable resolution engine.
"""
from __future__ import annotations
import os
import re
import uuid
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict

_PATTERN = re.compile(r"\$\{([^{}]+)\}")

class RequestNormalizer:

    @staticmethod
    def normalize(request):
        request.path = request.path.strip()
        if request.headers:
            request.headers = {
                k.strip(): (
                    v.strip() if isinstance(v, str) else v
                )
                for k, v in request.headers.items()
            }
        if request.query:
            request.query = {
                k.strip(): (
                    v.strip() if isinstance(v, str) else v
                )
                for k, v in request.query.items()
            }
        return request
 
class VariableResolver:
    def __init__(
        self,
        environment: Dict[str, Any],
        variables: Dict[str, Any]
    ):
        self.environment = environment or {}
        self.variables = variables or {}
    # --------------------------------------------------
    def resolve(self, value: Any) -> Any:
        """
        Resolve variables recursively.
        """
        if value is None:
            return None
        if isinstance(value, str):
            return self._resolve_string(value)
        if isinstance(value, dict):
            return {
                key: self.resolve(item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [
                self.resolve(item)
                for item in value
            ]
        return value
    # --------------------------------------------------
    def _resolve_string(
        self,
        text: str
    ) -> str:
        while True:
            match = _PATTERN.search(text)
            if not match:
                break
            placeholder = match.group(1)
            replacement = self._resolve_placeholder(
                placeholder
            )
            text = text.replace(
                "${%s}" % placeholder,
                replacement
            )
        return text
    # --------------------------------------------------
    def _resolve_placeholder(
        self,
        placeholder: str
    ) -> str:
        #
        # UUID
        #
        if placeholder == "uuid":
            return str(
                uuid.uuid4()
            )
        #
        # DATE
        #
        if placeholder.startswith("date:"):
            pattern = placeholder[5:]
            return datetime.now().strftime(
                self._convert_date(pattern)
            )
        #
        # ENVIRONMENT
        #
        if placeholder.startswith("env:"):
            key = placeholder[4:]
            return str(
                self.environment.get(
                    key,
                    ""
                )
            )
        #
        # VARIABLES
        #
        if placeholder.startswith("var:"):
            key = placeholder[4:]
            return str(
                self.variables.get(
                    key,
                    ""
                )
            )
        #
        # SYSTEM
        #
        if placeholder.startswith("sys:"):
            key = placeholder[4:]
            return str(
                os.environ.get(
                    key,
                    ""
                )
            )
        #
        # Unknown
        #
        return "${%s}" % placeholder
    # --------------------------------------------------
    @staticmethod
    def _convert_date(
        pattern: str
    ) -> str:
        mapping = {
            "yyyy": "%Y",
            "MM": "%m",
            "dd": "%d",
            "HH": "%H",
            "mm": "%M",
            "ss": "%S"
        }
        result = pattern
        for java, python in mapping.items():
            result = result.replace(
                java,
                python
            )
        return result
    # --------------------------------------------------
    def resolve_request(
        self,
        request
    ):
        """
        Returns a deep-copied request with all
        variables resolved.
        """
        request = deepcopy(request)
        request.path = self.resolve(
            request.path
        )
        
        # strip trail whitespace from the url
        #request.path = str(request.path).strip()
        
        request.headers = self.resolve(
            request.headers
        )
        request.query = self.resolve(
            request.query
        )
        request.body = self.resolve(
            request.body
        )
        
        request = RequestNormalizer.normalize(request)
        
        return request
 
    # --------------------------------------------------

    def resolve_environment(self) -> Dict[str, Any]:
        """
        Resolve environment variables that reference
        other environment variables.
        Example:
        HOST=company.com
        BASE=https://${env:HOST}
        API=${env:BASE}/api
        """
        resolved = dict(self.environment)
        max_iterations = 20
        for _ in range(max_iterations):
            changed = False
            for key, value in resolved.items():
                if not isinstance(value, str):
                    continue
                new_value = self._resolve_env_string(
                    value,
                    resolved
                )
                if new_value != value:
                    resolved[key] = new_value
                    changed = True
            if not changed:
                break
        else:
            raise ValueError(
                "Circular environment variable reference detected."
            )
        self.environment = resolved
        return resolved

    # --------------------------------------------------
    @staticmethod
    def _resolve_env_string(
        text: str,
        environment: Dict[str, Any]
    ) -> str:
        pattern = re.compile(r"\$\{env:([^{}]+)\}")
        while True:
            match = pattern.search(text)
            if not match:
                break
            key = match.group(1)
            value = str(
                environment.get(
                    key,
                    ""
                )
            )
            text = text.replace(
                match.group(0),
                value
            )
        return text
 