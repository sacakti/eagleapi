"""
Request execution engine.
"""
from __future__ import annotations
from pathlib import Path
from typing import List, Optional
from framework.client import HttpClient
from framework.constants import ReportStatus
from framework.loader import RequestLoader
from framework.models import ExecutionResult
from framework.response import ResponseWriter
from framework.validator import Validator
from framework.variables import VariableResolver
class Runner:
    def __init__(
        self,
        context
    ):
        self._context = context
        self._loader = RequestLoader(
            Path.cwd()
        )
        self._client = HttpClient(
            context.environment
        )
        self._writer = ResponseWriter(
            Path.cwd()
        )
        self._validator = Validator()
        self._resolver = VariableResolver(
            environment=context.configuration.environment,
            variables=context.variables
        )
        #
        # Resolve environment variables once.
        #
        self._resolver.resolve_environment()
        self._statistics = context.statistics
        self._logger = context.logger
        self._dashboard = getattr(
            context,
            "dashboard",
            None
        )
    # --------------------------------------------------
    def run_request(
        self,
        endpoint: str,
        request_name: str,
        save_response: bool = True,
        response_filename: Optional[str] = None
    ) -> ExecutionResult:
        response_file = None
        try:
            #
            # Dashboard
            #
            if self._dashboard:
                self._dashboard.phase(
                    "Loading Request"
                )
            #
            # Load request
            #
            request = self._loader.load(
                endpoint,
                request_name
            )
            #
            # Resolve variables
            #
            request = self._resolver.resolve_request(
                request
            )
            if self._dashboard:
                self._dashboard.request(
                    request_name=request_name,
                    method=request.method.value,
                    url=request.path
                )
                self._dashboard.phase(
                    "Sending Request"
                )
            self._logger.info(
                f"[{request.method.value}] "
                f"{request.path}"
            )
            #
            # Execute HTTP request
            #
            response = self._client.execute(
                request
            )
            #
            # Dashboard update
            #
            if self._dashboard:
                self._dashboard.phase(
                    "Response Received"
                )
                self._dashboard.response(
                    status=str(
                        response.status_code
                    ),
                    response_time=response.elapsed_ms,
                    response_size=response.size_bytes
                )
            #
            # Validate
            #
            validation = self._validator.validate(
                request.assertions,
                response
            )
            status = (
                ReportStatus.PASSED
                if validation.passed
                else ReportStatus.FAILED
            )
            #
            # Save response
            #
            if save_response:
                response_file = self._writer.save(
                    endpoint=endpoint,
                    request_name=request_name,
                    response=response,
                    filename=response_filename
                )
            #
            # Build execution result
            #
            result = ExecutionResult(
                endpoint=endpoint,
                request_name=request_name,
                status=status,
                http_status=response.status_code,
                response_time_ms=response.elapsed_ms,
                response_size=response.size_bytes,
                response_headers=response.headers,
                response_body=response.body,
                response_file=(
                    str(response_file)
                    if response_file
                    else None
                )
            )
            #
            # Statistics
            #
            self._statistics.add(
                result
            )
            #
            # Dashboard statistics
            #
            if self._dashboard:
                summary = (
                    self._statistics.summary
                )
                self._dashboard.statistics(
                    passed=summary.passed,
                    failed=summary.failed,
                    average=summary.average_response_time,
                    fastest=summary.fastest_response,
                    slowest=summary.slowest_response
                )
            self._logger.info(
                f"{response.status_code} "
                f"{response.elapsed_ms:.2f} ms"
            )
            #self. _statistics.finish()
            return result
        except Exception as ex:
            self._logger.exception(
                ex
            )
            if self._dashboard:
                self._dashboard.event(
                    str(ex)
                )
            result = ExecutionResult(
                endpoint=endpoint,
                request_name=request_name,
                status=ReportStatus.FAILED,
                error_message=str(ex)
            )
            self._statistics.add(
                result
            )
            return result
    
    # --------------------------------------------------
    def run_all(
        self,
        endpoint: str,
        save_response: bool = True
    ) -> List[ExecutionResult]:
        results: List[ExecutionResult] = []
        requests = self._loader.list_requests(
            endpoint
        )
        if self._dashboard:
            self._dashboard.phase(
                "Preparing Execution"
            )
            self._dashboard.progress_start(
                total=len(requests),
                description="Executing Requests"
            )
        try:
            for request_name in requests:
                if self._dashboard:
                    self._dashboard.phase(
                        "Executing"
                    )
                result = self.run_request(
                    endpoint=endpoint,
                    request_name=request_name,
                    save_response=save_response
                )
                results.append(result)
                if self._dashboard:
                    self._dashboard.progress_update(
                        request_name
                    )
            return results
        finally:
            self._statistics.finish()
            if self._dashboard:
                summary = self._statistics.summary
                self._dashboard.statistics(
                    passed=summary.passed,
                    failed=summary.failed,
                    average=summary.average_response_time,
                    fastest=summary.fastest_response,
                    slowest=summary.slowest_response
                )
                self._dashboard.phase(
                    "Completed"
                )
                self._dashboard.progress_stop()
            self._logger.info("")
            self._logger.info(
                "=" * 70
            )
            self._logger.info(
                "Execution Summary"
            )
            summary = self._statistics.summary
            self._logger.info(
                f"Total Requests : {summary.total_requests}"
            )
            self._logger.info(
                f"Passed         : {summary.passed}"
            )
            self._logger.info(
                f"Failed         : {summary.failed}"
            )
            self._logger.info(
                "Average        : "
                f"{summary.average_response_time:.2f} ms"
            )
            self._logger.info(
                "Fastest        : "
                f"{summary.fastest_response:.2f} ms"
            )
            self._logger.info(
                "Slowest        : "
                f"{summary.slowest_response:.2f} ms"
            )
            self._logger.info(
                "=" * 70
            )
            #
            # Close HTTP session
            #
            try:
                self._client.close()
            except Exception:
                pass

    # --------------------------------------------------
    @property
    def statistics(self):
        return self._statistics.summary