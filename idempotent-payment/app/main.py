from fastapi import FastAPI, Header, HTTPException
from app.database import SessionLocal
from app.schemas import PaymentRequest
from app.service import process_payment

# Initialize FastAPI application
app = FastAPI()

@app.post("/payments")
def pay(
    payload: PaymentRequest,
    idempotency_key: str = Header(...)
):
    """
    Payment API endpoint.

    Key ideas:
    - Accepts a payment request body (user_id, amount)
    - Requires an Idempotency-Key header
    - Safely handles retries without double-charging
    """

    # Create a new database session for this request
    db = SessionLocal()

    try:
        # Process the payment using idempotent business logic
        payment = process_payment(
            db,
            payload.user_id,
            payload.amount,
            idempotency_key
        )

        # Return a consistent response
        # Even on retries, the same payment result is returned
        return {
            "payment_id": payment.id,
            "status": payment.status,
            "amount": payment.amount
        }

    finally:
        # Always close the DB session
        # Prevents connection leaks under high traffic
        db.close()
