"""
Framework event definitions.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict

class EventType(str, Enum):
    APPLICATION_STARTED = "APPLICATION_STARTED"
    APPLICATION_FINISHED = "APPLICATION_FINISHED"
    CONFIGURATION_LOADING = "CONFIGURATION_LOADING"
    CONFIGURATION_LOADED = "CONFIGURATION_LOADED"
    ENDPOINT_SELECTED = "ENDPOINT_SELECTED"
    REQUEST_LOADING = "REQUEST_LOADING"
    REQUEST_LOADED = "REQUEST_LOADED"
    CONNECTION_OPENING = "CONNECTION_OPENING"
    CONNECTION_OPENED = "CONNECTION_OPENED"
    BEFORE_REQUEST = "BEFORE_REQUEST"
    AFTER_REQUEST = "AFTER_REQUEST"
    RESPONSE_RECEIVED = "RESPONSE_RECEIVED"
    RESPONSE_SAVED = "RESPONSE_SAVED"
    VALIDATION_STARTED = "VALIDATION_STARTED"
    VALIDATION_COMPLETED = "VALIDATION_COMPLETED"
    REPORT_GENERATED = "REPORT_GENERATED"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

@dataclass
class Event:
    event_type: EventType
    message: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)