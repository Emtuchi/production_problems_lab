# shard_health.py
# -------------------------------
# Tracks the health status of database shards
# -------------------------------

class ShardHealthRegistry:
    """
    Maintains a simple in-memory registry of shard health.
    
    Why it matters:
    - Enables fault-tolerant routing by avoiding unhealthy shards
    - Supports zero-downtime operations in distributed databases
    - Can be integrated with consistent hashing for dynamic routing
    """
    def __init__(self, shard_ids):
        """
        Initialize all shards as healthy by default.

        shard_ids: list of shard IDs to track
        """
        # status maps shard_id -> True (healthy) / False (down)
        self.status = {shard_id: True for shard_id in shard_ids}

    def mark_down(self, shard_id: int):
        """
        Mark a shard as unhealthy.

        Why it matters:
        - Prevents routing traffic to failing or unreachable shards
        """
        self.status[shard_id] = False

    def mark_up(self, shard_id: int):
        """
        Mark a shard as healthy.

        Why it matters:
        - Returns a previously failing shard to the rotation once it recovers
        """
        self.status[shard_id] = True

    def is_healthy(self, shard_id: int) -> bool:
        """
        Check if a shard is currently healthy.

        Returns:
            True if shard is healthy, False otherwise
        """
        return self.status.get(shard_id, False)

    def healthy_shards(self):
        """
        Return a list of all currently healthy shards.

        Why it matters:
        - Used by consistent hashing to rebuild the hash ring dynamically
        - Ensures only healthy shards receive traffic
        """
        return [s for s, ok in self.status.items() if ok]
