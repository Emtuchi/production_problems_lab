from fastapi import FastAPI, HTTPException
from db import get_session, engines
from models import Base, User
from shard_router import get_shard_id

# Initialize FastAPI application
app = FastAPI()

# Create tables on all shard databases at startup
# In real production systems, this would be handled by migrations,
# not automatically on application boot
for engine in engines.values():
    Base.metadata.create_all(bind=engine)

@app.post("/users")
def create_user(name: str, email: str):
    """
    Create a new user and route the write to the correct shard.

    This demonstrates application-level sharding, where the app
    (not the database) decides where data is stored.
    """

    # Generate a deterministic user_id based on email
    # This simulates ID generation for demo purposes
    # In production, IDs usually come from a central ID service or database
    user_id = abs(hash(email)) % 10_000

    # Determine which shard this user belongs to
    shard_id = get_shard_id(user_id)

    # Open a database session for the chosen shard
    db = get_session(shard_id)

    # Create and persist the user on the selected shard
    user = User(id=user_id, name=name, email=email)
    db.add(user)
    db.commit()

    return {
        "message": "User created successfully",
        "user_id": user_id,
        "shard": shard_id
    }

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Fetch a user from the correct shard.

    Reads must be routed to the same shard that handled the write,
    otherwise the user will not be found.
    """

    # Determine shard based on user_id
    shard_id = get_shard_id(user_id)

    # Open session for the correct shard
    db = get_session(shard_id)

    # Query the user from that shard only
    user = db.query(User).filter(User.id == user_id).first()

    # If the user does not exist on this shard, return 404
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "shard": shard_id
    }

@app.get("/shards/status")
def shard_status():
    """
    Return the number of users stored in each shard.

    Useful for visualizing shard distribution and detecting imbalance.
    """
    result = {}

    # Count rows in the users table on each shard
    for shard_id in engines.keys():
        db = get_session(shard_id)
        count = db.query(User).count()
        result[f"shard_{shard_id}"] = count

    return result
