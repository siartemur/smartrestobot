from app.interfaces.billing.billing_service import BillingService

class StripeBillingService(BillingService):
    def create_customer(self, email: str) -> str:
        # TODO: Stripe API ile entegrasyon
        print(f"[Stripe] Müşteri oluşturuldu: {email}")
        return "stripe_customer_id"

    def create_subscription(self, customer_id: str, plan_id: str) -> str:
        # TODO: Stripe API ile abonelik oluştur
        print(f"[Stripe] Abonelik oluşturuldu: {customer_id}, Plan: {plan_id}")
        return "stripe_subscription_id"

    def cancel_subscription(self, subscription_id: str) -> None:
        # TODO: Stripe API ile aboneliği iptal et
        print(f"[Stripe] Abonelik iptal edildi: {subscription_id}")
