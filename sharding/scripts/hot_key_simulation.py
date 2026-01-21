# -------------------------------------------
# Simulate hot key traffic distribution
# -------------------------------------------

from shard_router import get_shard_id  # Function to map a user ID to its shard
from collections import defaultdict     # For counting requests per shard
import random                           # For simulating random traffic

def simulate_hot_keys(total_users=1000, total_requests=10000):
    """
    Simulates traffic hitting a sharded system where some users are "hot keys"
    (receive disproportionately more requests than others).

    Parameters:
    - total_users: Number of unique users in the system.
    - total_requests: Total number of requests to simulate.
    
    This helps visualize shard load imbalance caused by hot keys.
    """
    
    # --------------------------
    # Select a few hot keys
    # --------------------------
    hot_keys = random.sample(range(total_users), k=5)  # Pick 5 popular users
    
    # --------------------------
    # Generate requests
    # --------------------------
    # 20% of traffic goes to hot users, 80% distributed randomly among all users
    requests = []
    for _ in range(total_requests):
        if random.random() < 0.2:  # 20% chance to hit a hot user
            requests.append(random.choice(hot_keys))
        else:
            requests.append(random.randint(0, total_users-1))
    
    # --------------------------
    # Count requests per shard
    # --------------------------
    shard_counter = defaultdict(int)  # shard_id -> request count
    
    for user_id in requests:
        shard_id = get_shard_id(user_id)  # Find shard for user
        shard_counter[shard_id] += 1      # Increment shard load counter
    
    # --------------------------
    # Display shard load distribution
    # --------------------------
    print("Shard load distribution:")
    for shard_id, count in sorted(shard_counter.items()):
        print(f"Shard {shard_id}: {count} requests")
    
    # --------------------------
    # Show which hot keys ended up on which shards
    # --------------------------
    print("\nHot keys hit counts per shard:")
    for hk in hot_keys:
        print(f"User {hk} on Shard {get_shard_id(hk)}")

# Run the simulation when executed as a script
if __name__ == "__main__":
    simulate_hot_keys()
