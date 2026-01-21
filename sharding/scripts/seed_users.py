from faker import Faker
from db import get_session
from models import User
from shard_router import get_shard_id

# Faker is used to generate realistic-looking test data
fake = Faker()

def seed_users(total=1000):
    """
    Populate the sharded databases with fake users.

    This helps demonstrate how users are distributed across shards
    based on the sharding strategy.
    """
    for i in range(total):
        # Use a deterministic user_id so shard routing is predictable
        user_id = i

        # Determine which shard this user belongs to
        shard_id = get_shard_id(user_id)

        # Open a session to the correct shard
        db = get_session(shard_id)

        # Create a fake user record
        user = User(
            id=user_id,
            name=fake.name(),
            email=f"user{i}@example.com"
        )

        # Persist the user to the selected shard
        db.add(user)
        db.commit()

    # Log completion summary
    print(f"Seeded {total} users across shards")

# Allow this script to be run directly from the command line
if __name__ == "__main__":
    seed_users()
