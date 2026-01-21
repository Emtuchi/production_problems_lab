from shard_router import ConsistentHashRing

# Initial shard setup (before scaling)
OLD_SHARDS = [0, 1, 2]

# New shard setup after adding one shard
NEW_SHARDS = [0, 1, 2, 3]

def simulate_rebalance(user_ids):
    """
    Simulates how many users would be reassigned to a different shard
    when the shard count changes using consistent hashing.

    This demonstrates the key benefit of consistent hashing:
    only a small fraction of keys move when a shard is added.
    """

    # Hash ring before scaling
    old_ring = ConsistentHashRing(OLD_SHARDS)

    # Hash ring after scaling
    new_ring = ConsistentHashRing(NEW_SHARDS)

    moved = 0  # Count how many users change shards

    for user_id in user_ids:
        # Determine shard assignment before scaling
        old = old_ring.get_shard(str(user_id))

        # Determine shard assignment after scaling
        new = new_ring.get_shard(str(user_id))

        # Count users that would need to be moved
        if old != new:
            moved += 1

    # Print how many users would require data movement
    print(f"{moved} / {len(user_ids)} users moved shards")

if __name__ == "__main__":
    # Run simulation for 10,000 users
    simulate_rebalance(range(10_000))
