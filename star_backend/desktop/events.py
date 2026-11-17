"""
Star Desktop Event System
Authoritative Reference: STAR_DESKTOP.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Callable, Any, Optional


@dataclass
class DesktopEvent:
    event_type: str  # "click", "change", "key", "resize", "custom"
    target_id: Optional[str] = None
    data: Any = None
    x: int = 0
    y: int = 0


class DesktopEventManager:
    def __init__(self):
        self.listeners: Dict[str, List[Callable[[DesktopEvent], None]]] = {}
        self.queue: List[DesktopEvent] = []

    def add_listener(self, event_type: str, callback: Callable[[DesktopEvent], None]):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def remove_listener(self, event_type: str, callback: Callable[[DesktopEvent], None]):
        if event_type in self.listeners:
            if callback in self.listeners[event_type]:
                self.listeners[event_type].remove(callback)

    def queue_event(self, event: DesktopEvent):
        self.queue.append(event)

    def dispatch(self, event: DesktopEvent):
        if event.event_type in self.listeners:
            for listener in list(self.listeners[event.event_type]):
                listener(event)

    def process_queue(self):
        while self.queue:
            ev = self.queue.pop(0)
            self.dispatch(ev)
