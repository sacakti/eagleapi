"""
Execution statistics collector.
"""

from __future__ import annotations
from datetime import datetime
from statistics import mean
from typing import List
from framework.constants import ReportStatus
from framework.models import ExecutionResult, Statistics

class StatisticsCollector:
    
    def __init__(self, execution_id: str):
        self._statistics = Statistics(
            execution_id=execution_id,
            start_time=datetime.now()
        )
        
    @property
    def summary(self) -> Statistics:
        return self._statistics
        
    @property
    def passed(self) -> int:
        return self._statistics.passed
    
    @property
    def failed(self) -> int:
        return self._statistics.failed
    
    @property
    def total(self) -> int:
        return self._statistics.total_requests
        
    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0
            
        return round(
            (self.passed / self.total) * 100,
            2
        )
        
        
    def add(self, result: ExecutionResult) -> None:
        self._statistics.results.append(result)
        self._statistics.total_requests += 1
        if result.status == ReportStatus.PASSED:
            self._statistics.passed += 1
        else:
            self._statistics.failed += 1
        self._recalculate()
            
    def finish(self) -> None:
        self._statistics.end_time = datetime.now()
        self._recalculate()
        self._statistics.total_execution_time = (
            self._statistics.end_time -
            self._statistics.start_time
        ).total_seconds() * 1000
        
        response_times: List[float] = [
            r.response_time_ms
            for r in self._statistics.results
        ]
        if response_times:
            self._statistics.average_response_time = round(
                mean(response_times),
                2
            )
            self._statistics.fastest_response = min(
                response_times
            )
            self._statistics.slowest_response = max(
                response_times
            )
    
    def _recalculate(self):
        response_times = [
            result.response_time_ms
            for result in self._statistics.results
        ]
        
        if not response_times:
            return
        
        self._statistics.average_response_time = round(
            mean(response_times),
            2
        )
        
        self._statistics.fastest_response = min(
            response_times
        )
        
        self._statistics.slowest_response = max(
            response_times
        )
        
        self._statistics.total_response_size = sum(
            result.response_size
            for result in self._statistics.results
        )