# -------------------------------------------
# Simulate shard failure and recovery impact
# -------------------------------------------

from shard_router import (
    get_shard_id,   # Function to map a user ID to its shard
    mark_shard_down, # Marks a shard as unhealthy
    mark_shard_up    # Marks a shard as healthy again
)

def simulate():
    """
    Simulates user routing under shard failure and recovery.
    Demonstrates how many users get re-routed when a shard goes down.
    """

    users = range(1000)  # Simulate 1000 user IDs

    # --------------------------
    # Baseline routing (all shards healthy)
    # --------------------------
    print("Initial routing:")
    baseline = {u: get_shard_id(u) for u in users}  # Map each user to its shard

    # --------------------------
    # Simulate shard failure
    # --------------------------
    print("Shard 1 fails...")
    mark_shard_down(1)  # Take shard 1 out of rotation

    # Check new routing after failure
    after_failure = {u: get_shard_id(u) for u in users}

    # Count how many users got re-routed due to shard failure
    moved = sum(
        1 for u in users if baseline[u] != after_failure[u]
    )
    print(f"{moved} users re-routed after shard failure")

    # --------------------------
    # Simulate shard recovery
    # --------------------------
    print("Shard 1 recovers...")
    mark_shard_up(1)  # Bring shard 1 back into rotation

if __name__ == "__main__":
    simulate()  # Run the simulation
