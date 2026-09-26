"""
Core data models used throughout the API Tester.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from framework.constants import HttpMethod, ReportStatus


class EndpointDefinition(BaseModel):
    name: str
    path: str
    request_count: int
    directory: str
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )
   
class Assertion(BaseModel):
    status: Optional[int] = None
    response_time: Optional[int] = Field(default=None, alias="responseTime")
    headers: Dict[str, Any] = Field(default_factory=dict)
    json: Dict[str, Any] = Field(default_factory=dict)
    body_contains: Optional[str] = Field(
        default=None,
        alias="bodyContains"
    )
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

class RequestDefinition(BaseModel):
    name: str
    method: HttpMethod
    path: str
    description: Optional[str] = ""
    headers: Dict[str, str] = Field(default_factory=dict)
    query: Dict[str, Any] = Field(default_factory=dict)
    body: Any = None
    assertions: Optional[Assertion] = None
    enabled:bool = True
    tags: List[str] = Field(default_factory=list)
    timeout: Optional[int] = None
    save_response:bool = Field(
        default=True,
        alias="saveResponse"
    )
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

class ResponseDefinition(BaseModel):
    status_code: int
    headers: Dict[str, str] = Field(default_factory=dict)
    url: Optional[str] = None
    method: Optional[str] = None
    body: Any = None
    elapsed_ms: float = 0
    size_bytes: int = 0
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

class ExecutionResult(BaseModel):
    endpoint: str
    request_name: str
    status: ReportStatus
    http_status: Optional[int] = None
    response_time_ms: float = 0
    response_size: int = 0
    response_file: Optional[str] = None
    error_message: Optional[str] = None
    response_headers: Dict[str, Any] = Field(default_factory=dict)
    response_body: Any = None
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

class Statistics(BaseModel):
    execution_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_requests: int = 0
    passed: int = 0
    failed: int = 0
    average_response_time: float = 0
    fastest_response: float = 0
    slowest_response: float = 0
    total_response_size: int = 0
    total_execution_time: float = 0
    results: List[ExecutionResult] = Field(default_factory=list)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

class Environment(BaseModel):
    name: str
    base_url: str
    verify_ssl: bool = True
    timeout: int = 30
    client_certificate: Optional[str] = None
    client_key: Optional[str] = None
    ca_certificate: Optional[str] = None
    proxy: Optional[str] = None
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )