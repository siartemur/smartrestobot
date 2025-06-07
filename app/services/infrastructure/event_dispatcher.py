from typing import Callable, Dict, List
from app.interfaces.infrastructure.event_dispatcher import EventDispatcher

class InMemoryEventDispatcher(EventDispatcher):
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def register_event(self, event_name: str, callback: Callable) -> None:
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def dispatch_event(self, event_name: str, *args, **kwargs) -> None:
        for callback in self._listeners.get(event_name, []):
            callback(*args, **kwargs)
