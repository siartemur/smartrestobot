from typing import Protocol, Callable

class EventDispatcher(Protocol):
    def register_event(self, event_name: str, callback: Callable) -> None:
        ...

    def dispatch_event(self, event_name: str, *args, **kwargs) -> None:
        ...
