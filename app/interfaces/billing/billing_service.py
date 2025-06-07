from typing import Protocol

class BillingService(Protocol):
    def create_customer(self, email: str) -> str:
        ...

    def create_subscription(self, customer_id: str, plan_id: str) -> str:
        ...

    def cancel_subscription(self, subscription_id: str) -> None:
        ...
