"""
Execution Context
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict
from requests import Session
from framework.eventbus import EventBus
from framework.statistics import StatisticsCollector
from framework.logger import Logger

@dataclass
class ExecutionContext:
    execution_id: str
    environment: Any
    configuration: Any
    logger: Logger
    statistics: StatisticsCollector
    event_bus: EventBus
    dashboard: Any = None
    session: Session = field(default_factory=Session)
    variables: Dict[str, Any] = field(default_factory=dict)