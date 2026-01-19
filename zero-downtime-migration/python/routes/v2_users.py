# routes/v2_users.py
# Defines version 2 of the Users API.
# This version uses the NEW schema (first_name / last_name),
# while still maintaining compatibility with the old schema
# through a dual-write strategy.

from fastapi import APIRouter
from database import SessionLocal
from models import User

# Create a router for v2 endpoints
router = APIRouter()

@router.post("/users")
def create_user_v2(first_name: str, last_name: str, email: str):
    # Create a new database session for this request
    db = SessionLocal()

    # Dual-write pattern:
    # New clients send first_name and last_name.
    # We also derive and write full_name so old systems,
    # reports, or background jobs continue to work.
    full_name = f"{first_name} {last_name}"

    # Create user with BOTH old and new columns populated
    user = User(
        first_name=first_name,
        last_name=last_name,
        full_name=full_name,  # legacy column
        email=email
    )

    # Persist the new user record
    db.add(user)
    db.commit()

    # Refresh instance to load generated fields (e.g., id)
    db.refresh(user)

    # Return response using ONLY the new schema
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

@router.get("/users/{user_id}")
def get_user_v2(user_id: int):
    # Create a database session
    db = SessionLocal()

    # Fetch user by primary key
    user = db.query(User).filter(User.id == user_id).first()

    # Return response in the new API format
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name
    }
