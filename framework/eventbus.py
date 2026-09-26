"""
Simple publish/subscribe event bus.
"""
from __future__ import annotations
from collections import defaultdict
from typing import Callable, Dict, List
from framework.events import Event, EventType

EventHandler = Callable[[Event], None]

class EventBus:
    def __init__(self):
        self._subscribers: Dict[
            EventType,
            List[EventHandler]
        ] = defaultdict(list)
    def subscribe(
        self,
        event_type: EventType,
        handler: EventHandler
    ) -> None:
        self._subscribers[event_type].append(handler)
    def publish(
        self,
        event: Event
    ) -> None:
        handlers = self._subscribers.get(
            event.event_type,
            []
        )
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                # UI should never crash execution
                pass
    def clear(self):
        self._subscribers.clear()