from typing import Protocol

class AuthProvider(Protocol):
    def login(self, email: str, password: str) -> str:
        ...

    def register(self, name: str, email: str, password: str) -> str:
        ...

    def verify_token(self, token: str) -> dict:
        ...
