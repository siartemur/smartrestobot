from typing import Protocol

class PasswordHasher(Protocol):
    def hash_password(self, password: str) -> str:
        ...

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        ...
