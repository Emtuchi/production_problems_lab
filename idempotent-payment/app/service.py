from sqlalchemy.exc import IntegrityError
from app.models import Payment, Wallet

def process_payment(db, user_id: int, amount: float, idem_key: str):
    """
    Core idempotent payment logic.

    Goal:
    - Ensure the same payment is never processed twice
    - Safely handle retries caused by network failures, timeouts, or client retries

    Strategy:
    - Attempt to insert a payment using a UNIQUE idempotency key
    - If the key already exists, the database raises an IntegrityError
    - On conflict, return the existing payment instead of charging again
    """

    try:
        # Create a new payment record with a unique idempotency key
        # If this key already exists, the DB will reject the insert
        payment = Payment(
            user_id=user_id,
            amount=amount,
            idempotency_key=idem_key,
            status="SUCCESS"
        )

        # Stage the payment insert
        db.add(payment)

        # Fetch the user's wallet
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()

        # If the wallet does not exist, create one with a zero balance
        # (Useful for first-time users)
        if not wallet:
            wallet = Wallet(user_id=user_id, balance=0)
            db.add(wallet)

        # Deduct the payment amount from the wallet balance
        # NOTE: This assumes sufficient balance checks happen earlier
        wallet.balance -= amount

        # Commit both the payment and wallet update as one transaction
        # Ensures atomicity: either both succeed or both fail
        db.commit()

        # Return the newly created payment
        return payment

    except IntegrityError:
        # Duplicate idempotency key detected
        # → This payment was already processed
        db.rollback()

        # Fetch and return the existing payment record
        # This guarantees the same response for repeated requests
        return db.query(Payment).filter(
            Payment.idempotency_key == idem_key
        ).first()
