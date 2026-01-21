import hashlib
import bisect
from shard_health import ShardHealthRegistry

# -------------------------------
# Consistent Hashing Implementation
# -------------------------------

class ConsistentHashRing:
    """
    Implements a consistent hashing ring for sharding.

    Consistent hashing allows:
    - Even distribution of keys across shards
    - Minimal key remapping when shards are added or removed
    - High availability and scalability in distributed systems
    """
    def __init__(self, replicas=100):
        """
        Initialize a hash ring with virtual nodes for smoother distribution.

        replicas: Number of virtual nodes per shard. More replicas = fewer hotspots.
        """
        self.replicas = replicas
        self.ring = {}          # Maps each hash value to a shard ID
        self.sorted_keys = []   # Sorted list of hashes for efficient O(log n) lookup

    def _hash(self, key: str) -> int:
        """
        Compute a stable hash for a string key using MD5.

        Why it matters: 
        - Ensures deterministic routing of keys to shards
        - Supports consistent hashing across multiple app instances
        """
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def build(self, shard_ids):
        """
        Construct the consistent hash ring using the provided shard IDs.

        Why it matters:
        - Assigns virtual nodes to each shard to prevent uneven key distribution
        - Clears and rebuilds the ring based on current healthy shards
        """
        self.ring.clear()
        self.sorted_keys.clear()

        for shard_id in shard_ids:
            for i in range(self.replicas):
                vnode = f"{shard_id}:{i}"           # Create a virtual node label
                h = self._hash(vnode)               # Hash the virtual node
                self.ring[h] = shard_id             # Map hash -> shard
                bisect.insort(self.sorted_keys, h)  # Keep the keys sorted for fast lookups

    def get_shard(self, key: str) -> int:
        """
        Determine which shard is responsible for a given key.

        How it works:
        - Hash the key
        - Use bisect to find the first hash in the ring >= key hash
        - Wrap around to the first shard if key exceeds all hashes

        Why it matters:
        - Ensures even distribution of data
        - Minimal key movement when shards change
        """
        h = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, h)

        if idx == len(self.sorted_keys):  # Wrap around the ring
            idx = 0

        return self.ring[self.sorted_keys[idx]]


# -------------------------------
# Global Routing & Health State
# -------------------------------

ALL_SHARDS = [0, 1, 2]                         # Initial set of shard IDs
health_registry = ShardHealthRegistry(ALL_SHARDS)  # Tracks which shards are healthy
hash_ring = ConsistentHashRing()               # Global consistent hash ring instance

def rebuild_ring():
    """
    Rebuild the hash ring using only currently healthy shards.

    Why it matters:
    - Prevents routing keys to unhealthy/down shards
    - Ensures high availability and fault tolerance
    """
    healthy = health_registry.healthy_shards()
    if not healthy:
        raise RuntimeError("No healthy shards available")
    hash_ring.build(healthy)

# Build the initial ring at startup
rebuild_ring()

def get_shard_id(user_id: int) -> int:
    """
    Determine the shard for a given user ID.

    Why it matters:
    - Centralizes routing logic
    - Guarantees deterministic routing for distributed storage
    """
    return hash_ring.get_shard(str(user_id))


# -------------------------------
# Shard Failure / Recovery API
# -------------------------------

def mark_shard_down(shard_id: int):
    """
    Mark a shard as unhealthy and rebuild the ring without it.

    Why it matters:
    - Automatically avoids routing traffic to failing shards
    - Supports graceful degradation without downtime
    """
    health_registry.mark_down(shard_id)
    rebuild_ring()

def mark_shard_up(shard_id: int):
    """
    Mark a shard as healthy and rebuild the ring including it.

    Why it matters:
    - Returns shard to rotation after recovery
    - Ensures consistent key routing resumes for that shard
    """
    health_registry.mark_up(shard_id)
    rebuild_ring()
