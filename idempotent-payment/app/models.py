from sqlalchemy import Column, Integer, Numeric, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Base class for all SQLAlchemy models
# - Stores metadata about tables
# - Required for SQLAlchemy to map Python classes to DB tables
Base = declarative_base()

class Wallet(Base):
    # Name of the database table
    __tablename__ = "wallets"

    # Primary key for the wallets table
    id = Column(Integer, primary_key=True)

    # Business identifier for the wallet owner
    # - Enforced as unique so each user has only one wallet
    user_id = Column(Integer, unique=True)

    # Current wallet balance
    # - Uses Numeric to avoid floating-point precision errors with money
    balance = Column(Numeric)

class Payment(Base):
    # Name of the database table
    __tablename__ = "payments"

    # Primary key for the payments table
    id = Column(Integer, primary_key=True)

    # ID of the user making the payment
    user_id = Column(Integer)

    # Amount for this payment
    # - Numeric ensures accurate financial calculations
    amount = Column(Numeric)

    # Unique key provided by the client to guarantee idempotency
    # - Prevents duplicate charges when requests are retried
    idempotency_key = Column(String, unique=True)

    # Current payment state (e.g. "pending", "completed", "failed")
    status = Column(String)

    # Timestamp for when the payment record was created
    # - Uses UTC to avoid timezone inconsistencies
    created_at = Column(DateTime, default=datetime.utcnow)
