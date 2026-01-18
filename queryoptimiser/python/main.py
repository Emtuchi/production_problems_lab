import time  # For measuring how long the query takes
from fastapi import FastAPI  # FastAPI web framework
from database import SessionLocal  # SQLAlchemy session factory to interact with the DB
from models import User  # User model (with relationships to Order and OrderItem)
from sqlalchemy.orm import joinedload  # Used for eager loading to reduce N+1 queries

# Initialize the FastAPI app
app = FastAPI()

# Define a GET endpoint at /users/{user_id}/orders
@app.get("/users/{user_id}/orders")
def get_user_orders_slow(user_id: int):
    # Record the start time to measure query duration
    start = time.time()
    
    # Create a new SQLAlchemy session (connection to DB)
    db = SessionLocal()

    # Fetch the user with the given user_id
    # .options(joinedload(User.orders)) tells SQLAlchemy to eagerly load orders
    # This reduces the N+1 query problem for the user's orders
    user = (
        db.query(User)
        .options(joinedload(User.orders))
        .filter(User.id == user_id)
        .first()
    )
    # Note: If user_id doesn't exist, `user` will be None and `user.orders` will fail

    # Build the response JSON
    # For each order of the user, collect its ID and list of product names
    result = [
        {
            "order_id": order.id,
            # Access order.items (relationship) and extract product_name for each item
            "items": [item.product_name for item in order.items]
        }
        for order in user.orders
    ]

    # Measure how long the query + processing took
    duration = time.time() - start

    # Return JSON response with query time and orders
    return {
        "query_time_seconds": duration,
        "orders": result
    }

