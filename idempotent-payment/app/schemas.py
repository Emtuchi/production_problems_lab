from pydantic import BaseModel

class PaymentRequest(BaseModel):
    user_id: int
    amount: float
