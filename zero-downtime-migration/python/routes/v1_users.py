# routes/v1_users.py
# Defines version 1 of the Users API.
# This version represents the OLD contract that existing clients still rely on.
# It continues to use the legacy `full_name` field to avoid breaking consumers
# during a zero-downtime migration.

from fastapi import APIRouter
from database import SessionLocal
from models import User

# Create a router for v1 endpoints
router = APIRouter()

@router.post("/users")
def create_user_v1(full_name: str, email: str):
    # Create a new database session for this request
    db = SessionLocal()

    # OLD API behavior:
    # Existing clients only send `full_name`, not first_name / last_name.
    # We continue writing to the legacy column so old clients keep working.
    user = User(full_name=full_name, email=email)

    # Persist the new user record
    db.add(user)
    db.commit()

    # Refresh the instance to load generated fields (e.g., id)
    db.refresh(user)

    # Return response in the OLD API format
    return {
        "id": user.id,
        "full_name": user.full_name
    }

@router.get("/users/{user_id}")
def get_user_v1(user_id: int):
    # Create a database session
    db = SessionLocal()

    # Fetch user by primary key
    user = db.query(User).filter(User.id == user_id).first()

    # Return only legacy fields expected by v1 clients
    return {
        "id": user.id,
        "full_name": user.full_name
    }
